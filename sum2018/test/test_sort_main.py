from test_sort_fft_draw import *

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

