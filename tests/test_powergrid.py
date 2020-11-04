
# def test_eval_powergrid():
#     """
#     result: list of incident_results
#     [
#     (user, accuraty (0 - not detected or 1 - detected), detection timeliness in second
#     ]
#     """
#     import datasets
#     import attack_sequencing
#     import experiment
#     result = []
#     # f = open('/tmp/test.txt', 'w')
#     for df, compromised_users in datasets.load_powergrid(): # for each incident
#         incident_result = []
#         for u in set(compromised_users):
#             # from pdb import set_trace; set_trace()
#             # add timestamp for stop and start
#             df_user = df[df['user'] == u].sort_index()
#             df_user_with_start_stop = datasets.add_start_stop_and_timestamp(df_user)
#             # build the event array for the user, converting raw events to number
#             E = df_user_with_start_stop['event']
#             # print >> f, df_user_with_start_stop
#             # break
#             print 'sequencing {}'.format(u)
#             y_hat, y_hat_pretty = attack_sequencing.sequence(E)
#             print y_hat_pretty
#             detection_timeliness = experiment.eval_detection_timeliness(df_user_with_start_stop,
#                                                        [(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
#             accuracy = experiment.eval_accuracy_compromised([(x[1],x[2]) for x in y_hat_pretty.label]) # extract only su and sa and print
#             incident_result.append((u, accuracy, detection_timeliness))
#         result.append(incident_result)
#     # f.close()
#     pickle.dump(result, open("powergrid.p","wb"))
#     return result
