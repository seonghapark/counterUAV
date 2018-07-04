from test_fft_draw import *

if __name__ == "__main__":
    pwd = os.getcwd() # current working folder

    # Declare objects of MyThread class
    file_name = pwd+ '/' +sys.argv[1]
    Thread1 = inwav_handler(file_name)
    Thread2 = fft_handler()

    # Start new Threads
    Thread1.start()
    Thread2.start()

    colorgraph = colorgraph_handler()
    colorgraph.draw_graph()

    # #inwav part
    # print("start inwav part")
    # file_name = pwd+ '/' +sys.argv[1]
    # inwav = inwav_handler(file_name)
    # print("end inwav part")

    # #fft part
    # print("start fft part")
    # fft = fft_handler()
    # count = 0
    # while(True):
    #     raw = inwav.get_chunk()
    #     if raw is None:
    #         break
    #     fft.get_line(raw)
    #     time, result = fft.data_process()
    #     fft.store_result()
    #     print("in fft", count, time.shape, result.shape)
    #     count+=1
    # print("end fft part")

