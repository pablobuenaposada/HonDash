# Public demo on a DigitalOcean droplet

The demo runs the backend against fake ECU data (`src/bench/demo.py`) so the
dashboard can be shown without a car. It is three containers, defined in
[`docker-compose.demo.yml`](../docker-compose.demo.yml):

| Service    | Published port | What it does                                                         |
|------------|----------------|----------------------------------------------------------------------|
| `app`      | 5678           | backend websocket, runs `src/bench/demo.py` from the published image |
| `nginx`    | none           | serves `schema.json`, only reachable from inside the compose network |
| `frontend` | 80             | the dashboard, built from the HonDash-frontend repo                  |

The browser loads the page from port 80 and then opens a websocket straight to
port 5678 on the same host, so **both ports have to be open to the world**. The
frontend proxies `/schema.json` to the `nginx` service internally, which is why
that one needs no published port.

## How this is split

The droplet is created **once, from your machine**. After that every push to
master redeploys onto that same droplet over ssh. CI never runs terraform, so it
can never create a second droplet, and there is nothing extra to pay for:
terraform state is a local file.

## Why plain HTTP

The frontend hardcodes `ws://` (`src/data.js`, `src/redirection.js` and four
other files in that repo). If the page were served over HTTPS the browser would
refuse the `ws://` connection as mixed content, so putting the demo behind TLS
means changing the frontend to use `wss://` first. The demo is HTTP only.

## One time: create the droplet

You need an SSH key uploaded to your DigitalOcean account (Settings → Security)
and a personal access token with Full Access (`api:write`).

```sh
ssh-keygen -t ed25519 -C hondash-demo -f ~/.ssh/hondash_demo -N ""
# upload ~/.ssh/hondash_demo.pub to DigitalOcean, note the name you give it
```

Then, from `deploy/terraform`:

```sh
cp terraform.tfvars.example terraform.tfvars
```

Open `deploy/terraform/terraform.tfvars` in any text editor and fill in your
DigitalOcean token and the name of your SSH key, then:

```sh
terraform init
terraform apply
```

Terraform creates its own DigitalOcean project, "HonDash demo" by default, and
puts the droplet and the reserved IP in it rather than leaving them loose in the
account default project. Rename it with `project_name` in `terraform.tfvars`.
Note terraform creates that project itself; if you already made one by hand with
the same name you will end up with two, since DigitalOcean allows duplicate
project names. Firewalls cannot belong to a project, so that one stays outside.

Terraform prints the address when it finishes. Cloud-init installs docker,
clones this repository to `/opt/hondash` and runs `deploy/deploy.sh`, so the
demo is live a couple of minutes later without any further action.

The address is a reserved IP, so it stays the same even if the droplet is ever
destroyed and recreated.

### Look after the state file

`terraform.tfstate` lands in `deploy/terraform/` and is gitignored, because it
contains the token. It is the only record that the droplet belongs to this
config. Keep a copy somewhere; if you lose it, terraform will no longer know the
droplet exists and a later `apply` would build a second one. Recovery is
possible with `terraform import` but it is easier to just not lose it.

## Set up automatic deploys

In GitHub → Settings → Secrets and variables → Actions:

| Kind     | Name            | Value                                                       |
|----------|-----------------|-------------------------------------------------------------|
| Variable | `DEMO_HOST`     | the address terraform printed                               |
| Secret   | `DEMO_SSH_KEY`  | contents of `~/.ssh/hondash_demo`, the **private** half      |

That is all CI needs. No DigitalOcean token, no object storage credentials.

## Deploying

**Deploy demo** runs automatically after **Push docker image to registry
(hub.docker.com)** succeeds on master. That ordering matters: the compose file
runs `pablobuenaposada/hondash:latest`, so deploying before the new image is
pushed would just redeploy the previous build.

It ssh's into the droplet, fast forwards `/opt/hondash` to `origin/master` and
then runs [`deploy/deploy.sh`](deploy.sh) from that checkout:

```sh
docker compose -f docker-compose.demo.yml pull --ignore-buildable
docker compose -f docker-compose.demo.yml up -d --build --remove-orphans
docker image prune -f
```

Because the deploy steps are versioned in the repository rather than baked into
the droplet, a change to how deploying works ships exactly like a change to the
application. `--ignore-buildable` is what stops compose trying to pull the
frontend, which is built from source rather than pulled.

After the deploy the workflow polls the frontend and `/schema.json` until they
answer, so a broken deploy fails the run. The same workflow can be triggered
manually to redeploy without pushing a new image.

## Running the demo stack locally

```sh
docker compose -f docker-compose.demo.yml up -d --build
```

Then open <http://localhost/>. This is the same stack the droplet runs. Note it
wants ports 80 and 5678, so stop anything already using them (`make docker/demo`
uses 5678 too).

## Things worth knowing

- **Anyone can change the demo setup.** The websocket exposes `save` and
  `reset`, and there is no authentication, so a visitor can edit the demo's
  configuration. It is not persisted outside the container, so restarting `app`
  puts it back to `default_setup.json`.
- **Changing the droplet itself** means running `terraform apply` from your
  machine again. Note `user_data` is under `ignore_changes`: editing the
  cloud-init would otherwise replace the droplet, and the deploy steps live in
  `deploy.sh` precisely so that never has to happen.
- **Destroying it**: `terraform destroy` from `deploy/terraform`. The reserved
  IP goes too, so `DEMO_HOST` would need updating if you rebuild.
- **Host key checking**: the deploy job uses `ssh-keyscan` and trusts whatever
  it gets back on first contact. Fine for a demo; pin the host key if not.
- **Cost**: one `s-1vcpu-1gb` droplet, changeable through the `droplet_size`
  variable. The reserved IP is free while attached to a running droplet.
- **Frontend changes** live in another repository and will not trigger a deploy
  here; they get picked up on the next deploy, or run **Deploy demo** by hand.
