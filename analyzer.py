
def analyze(sniffer_conn, enforcer_conn, ruleset=None):
    pass


def load_ruleset(path):
    pass


def main():

    while True:

        packet = sniffer_conn.recv()

        # Pass packet through tests

        flag = False

        # Pass to enforcer