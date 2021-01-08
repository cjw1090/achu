import chrome_cache.calc_hash as calc_hash
from chrome_cache import browser_analysis
import os


class Browser:
    class History:
        def file_open(path):
            file = path.split("\\")[-1]
            if file == "History":
                return Browser.Chrome.History.file_open(path)
            elif file == "places.sqlite":
                return Browser.Firefox.History.file_open(path)
            elif file == "WebCacheV01.dat":
                return Browser.Ie_Edge.History.file_open(path)
            else:
                print("[Error] input file error by fortools\nPlease check your file")
                return -1

    class Cache:
        def file_open(path):
            file = path.split("\\")[-1]
            if file == "Cache":
                return Browser.Chrome.Cache.file_open(path)
            elif file == "WebCacheV01.dat":
                return Browser.Ie_Edge.Cache.file_open(path)
            else:
                print("[Error] input file error by fortools\nPlease check your file")
                return -1

    class Download:
        def file_open(path):
            file = path.split("\\")[-1]
            if file == "History":
                return Browser.Chrome.Download.file_open(path)
            elif file == "places.sqlite":
                return Browser.Firefox.Download.file_open(path)
            elif file == "WebCacheV01.dat":
                return Browser.Ie_Edge.Download.file_open(path)
            else:
                print("[Error] input file error by fortools\nPlease check your file")
                return -1

    class Cookie:
        def file_open(path):
            file = path.split("\\")[-1]
            if file == "Cookie":
                return Browser.Chrome.Cookie.file_open(path)
            elif file == "cookies.sqlite":
                return Browser.Firefox.Cookie.file_open(path)
            elif file == "WebCacheV01.dat":
                return Browser.Ie_Edge.Cookie.file_open(path)
            else:
                print("[Error] input file error by fortools\nPlease check your file")
                return -1

    class Chrome:
        class History:
            def file_open(path):
                hash_v = calc_hash.get_hash(path, 'before')
                chrome_file = browser_analysis.Chrome.History(path, hash_v)
                return chrome_file

        class Download:
            def file_open(path):
                hash_v = calc_hash.get_hash(path, 'before')
                chrome_file = browser_analysis.Chrome.Download(path, hash_v)
                return chrome_file

        class Cookie:
            def file_open(path):
                hash_v = calc_hash.get_hash(path, 'before')
                chrome_file = browser_analysis.Chrome.Cookie(path, hash_v)
                return chrome_file

        class Cache:
            def file_open(path):
                before_hash = []
                if os.path.exists(path):
                    cache_file_list = os.listdir(path)
                for i in range(0, len(cache_file_list)):
                    hashdic = {cache_file_list[i]: calc_hash.get_hash(
                        path+'\\'+cache_file_list[i], 'before')}
                    before_hash.append(hashdic)
                chrome_file = browser_analysis.Chrome.Cache(path, before_hash)
                return chrome_file
