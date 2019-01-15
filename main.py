Clock = multiprocessing.Value('i',1) #Définition de la shared memory

tick = ClockTick(Clock)
tick.start()
jour = multiprocessing.Value('i', 0)
Weather = multiprocessing.Array('i', [0, 0])
MessageQueueMarket = sysv_ipc.MessageQueue(128, sysv_ipc.IPC_CREAT)
#message = str(value).encode()
   # mq.send(message)