def pichunter():
    import re


    n = 0

    home = 'G:/Desktop/py/PICHUNTER_OVER_TOR/'
    
    urls = [
        # 'https://www.pichunter.com/models/Brandy_Blair',
        'https://www.pichunter.com/models/Hanna%2527s_Honeypot/photos/' # 6 pages
    ]

    number_of_pages = 6
    
    site_root = 'https://www.pichunter.com'

    proxies = {
        'http': 'socks5h://127.0.0.1:9150', 
        'https': 'socks5h://127.0.0.1:9150'
    }

    for page in range(1, number_of_pages+1):
        page_ = urls[0] + str(n)
        model_name = re.match(r'^.*models/(.*)/photos', urls[0]).group(1)
        
        if not os.path.exists(home + model_name):
            os.mkdir(home + model_name, mode=0o777)

        session = requests.Session()
        r = session.get(page_, proxies=proxies, stream=True)
        # print(r.text)

        soup = bs(r.content, 'html.parser')

        # write all albums in txt
        # f = open('G:/Desktop/Briana_albums.txt', 'w')
        albums = soup.find_all('a', attrs={'class': 'thumb pop-execute'})
        for album in albums:
            
            album_link = site_root + album['href'].strip()
            # /gallery/3605902/Big_titted_blonde_schoolgirl_Brandy#12
            # result: Big_titted_blonde_schoolgirl_Brandy
            album_title = re.match(r'^.*\/(.*)#.*', album_link).group(1)

            print(album_title)
            
            print('=' * 12)
            print(album_link)
            print('=' * 12)

            r = session.get(album_link, proxies=proxies, stream=True)
            soup = bs(r.content, 'html.parser')
            imgs_ = soup.find_all('img', attrs={'class': 'imgitem pop-execute'})

            for img_ in imgs_:
                
                # get the bigger pic from "src" by getting the needed url
                img_src_ = img_['src'].replace('i.jpg', 'o.jpg')
                print(img_src_)

                img_r_ = session.get(img_src_, proxies=proxies)
                con = img_r_.content
                outf = open(home + model_name + '/' + album_title + '_' + str(n) + '.jpg', "wb")
                outf.write(con)
                outf.close()

                n += 1

            n = 0
        
        page += 1

pichunter()
