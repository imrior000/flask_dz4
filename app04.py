import threading, sys, requests, multiprocessing, asyncio, time

def downloader(link):
    temp = link.split(".")
    ras = temp[-1]
    temp = temp[-2].split('/')
    name = temp[-1]
    time_start = time.time()
    r = requests.get(link)
    with open(name + "." + ras, "wb") as code:
        code.write(r.content)
    print("Файл - " + name + "." + ras + " скачан за - " + str(time.time() - time_start) + ' сек.')

async def async_downloader(link):
    downloader(link)

async def asyncr(links):
    tasks = []
    for i in range(len(links)):
        a = asyncio.create_task(async_downloader(links[i]))
        await a

if __name__ == '__main__':
    links = sys.argv[1:]
    mod = 'async'
    match mod:
        case 'process':
            processes_list = []
            for i in range(len(links)):
                link = links[i]
                p = multiprocessing.Process(target=downloader, args=(link,))
                processes_list.append(p)
                p.start()
                for p in processes_list:
                    p.join()
        case 'potok':
            threads = []
            for i in range(len(links)):
                t = threading.Thread(target=downloader, args=(links[i],))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
        case 'async':
            asyncio.run(asyncr(links))
    
   

