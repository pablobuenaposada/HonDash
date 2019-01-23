from git import Repo, exc


class Version:
    def __init__(self):
        self.repo = Repo('.')

    def get_current_tag(self):
        try:
            return self.repo.git.describe()
        except exc.GitCommandError:
            return 'Unknown'
