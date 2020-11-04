
def test_graphcrf():
    import attack_sequencing 
    # test events
    E = [
        SE.start,
        SE.login,
        SE.compile,
        SE.delete,
        SE.stop
        ]
    # test labels
    L = [
(SU.benign, SA.benign),
        (SU.benign, SA.benign),
        (SU.benign, SA.benign),
        (SU.suspicious, SA.prepare_attack),
        (SU.benign, SA.benign),
        ]
    y_hat, y_hat_pretty = attack_sequencing.sequence(E)
    print y_hat
    print y_hat_pretty
