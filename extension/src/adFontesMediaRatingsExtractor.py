import asyncio
from playwright.async_api import async_playwright
import json

name_mapping = {
    "www_readtangle_com": "Read Tangle",
    "cjr_org": "CJR",
    "www_cnn_com": "CNN",
    "foxnews_com": "Fox News",
    "www_vox_com": "Vox",
    "www_politico_com": "Politico",
    "thedispatch_com": "The Dispatch",
    "outkick_com": "Outkick",
    "poynter_org": "Poynter",
    "www_dailysignal_com": "The Daily Signal",
    "time_com": "Time",
    "rt_com": "RT",
    "www_theguardian_com": "The Guardian",
    "www_nytimes_com": "The New York Times",
    "www_bloomberg_com": "Bloomberg",
    "www_breitbart_com": "Breitbart",
    "www_npr_org": "NPR",
    "www_washingtonexaminer_com": "Washington Examiner",
    "www_motherjones_com": "Mother Jones",
    "theroot_com": "The Root",
    "fivethirtyeight_com": "FiveThirtyEight",
    "reason_com": "Reason",
    "thehill_com": "The Hill",
    "slate_com": "Slate",
    "www_infowars_com": "InfoWars",
    "newsday_com": "Newsday",
    "bipartisanreport_com": "Bipartisan Report",
    "americanlibertyemail_com": "American Liberty",
    "thepostemail_com": "The Post & Email",
    "climate_news": "Climate News",
    "arkansasonline_com": "Arkansas Online",
    "tpusa_com": "Turning Point USA",
    "city_journal_org": "City Journal",
    "thecentersquare_com": "The Center Square",
    "www_dailymail_co_uk": "Daily Mail",
    "www_latimes_com": "LA Times",
    "heritage_org": "Heritage Foundation",
    "businessinsider_com": "Business Insider",
    "mercola_com": "Mercola",
    "www_newsmax_com": "Newsmax",
    "www_oann_com": "OANN",
    "occupydemocrats_com": "Occupy Democrats",
    "www_dailywire_com": "The Daily Wire",
    "naturalnews_com": "Natural News",
    "www_washingtonpost_com": "The Washington Post",
    "activistpost_com": "Activist Post",
    "www_cbsnews_com": "CBS News",
    "bigleaguepolitics_com": "Big League Politics",
    "billoreilly_com": "Bill O'Reilly",
    "beforeitsnews_com": "Before It's News",
    "teenvogue_com": "Teen Vogue",
    "suntimes_com": "Chicago Sun-Times",
    "www_csmonitor_com": "The Christian Science Monitor",
    "cnbc_com": "CNBC",
    "newrepublic_com": "The New Republic",
    "amgreatness_com": "American Greatness",
    "www_bbc_com": "BBC",
    "www_theweek_com": "The Week",
    "thefederalist_com": "The Federalist",
    "chron_com": "Houston Chronicle",
    "tmz_com": "TMZ",
    "zerohedge_com": "Zero Hedge",
    "thebulwark_com": "The Bulwark",
    "realclearpolitics_com": "RealClearPolitics",
    "judicialwatch_org": "Judicial Watch",
    "weather_com": "The Weather Channel",
    "apnews_com": "AP News",
    "deseret_com": "Deseret News",
    "www_reuters_com": "Reuters",
    "msnbc_com": "MSNBC",
    "wsws_org": "World Socialist Web Site",
    "www_cnn_com_shows_situation_room": "CNN Situation Room",
    "www_cnn_com_shows_ac_360": "CNN AC 360",
    "www_foxnews_com_shows_fox_and_friends": "Fox & Friends",
    "www_foxnews_com_shows_hannity": "Hannity",
    "www_foxnews_com_shows_ingraham_angle": "The Ingraham Angle",
    "www_msnbc_com_the_last_word": "The Last Word",
    "www_foxnews_com_shows_special_report": "Special Report",
    "www_msnbc_com_rachel_maddow_show": "The Rachel Maddow Show",
    "www_msnbc_com_all": "All In with Chris Hayes",
    "tyt_com": "The Young Turks",
    "www_youtube_com_tytconversation": "TYT Conversation",
    "www_cbs_com_shows_cbs_evening_news": "CBS Evening News",
    "www_wsj_com": "The Wall Street Journal",
    "www_nbc_com_the_reidout": "The ReidOut",
    "newsweek_com": "Newsweek",
    "abcnews_go_com": "ABC News",
    "foreignpolicy_com": "Foreign Policy",
    "www_nbcnews_com": "NBC News",
    "www_usatoday_com": "USA Today",
    "www_nationalreview_com": "National Review",
    "nypost_com": "New York Post",
    "www_aljazeera_com": "Al Jazeera",
    "www_alternet_org": "AlterNet",
    "www_thegatewaypundit_com": "The Gateway Pundit",
    "townhall_com": "Townhall",
    "jezebel_com": "Jezebel",
    "www_theatlantic_com": "The Atlantic",
    "rollingstone_com": "Rolling Stone",
    "www_marketwatch_com": "MarketWatch",
    "www_axios_com": "Axios",
    "www_theblaze_com": "The Blaze",
    "wired_com": "Wired",
    "nydailynews_com": "New York Daily News",
    "www_huffpost_com": "HuffPost",
    "www_thenation_com": "The Nation",
    "www_thedailybeast_com": "The Daily Beast",
    "dailycaller_com": "The Daily Caller",
    "www_dailykos_com": "Daily Kos",
    "www_newyorker_com_news": "The New Yorker",
    "voanews_com": "Voice of America",
    "www_economist_com": "The Economist",
    "www_democracynow_org": "Democracy Now!",
    "quillette_com": "Quillette",
    "rasmussenreports_com": "Rasmussen Reports",
    "www_newsbusters_org": "NewsBusters",
    "salon_com": "Salon",
    "spectator_org": "The American Spectator",
    "talkingpointsmemo_com": "Talking Points Memo",
    "www_redstate_com": "RedState",
    "www_propublica_org": "ProPublica",
    "www_pbs_org": "PBS",
    "truthout_org": "Truthout",
    "twitchy_com": "Twitchy",
    "www_vanityfair_com": "Vanity Fair",
    "news_vice_com_en_us": "Vice News",
    "washingtonmonthly_com": "Washington Monthly",
    "prageru_com": "PragerU",
    "bostonglobe_com": "The Boston Globe",
    "cnsnews_com": "CNS News",
    "commondreams_org": "Common Dreams",
    "consortiumnews_com": "Consortium News",
    "ijr_com": "Independent Journal Review",
    "inquisitr_com": "Inquisitr",
    "inthesetimes_com": "In These Times",
    "miamiherald_com": "Miami Herald",
    "upi_com": "UPI",
    "usnews_com": "U.S. News & World Report",
    "counterpunch_org": "CounterPunch",
    "crooksandliars_com": "Crooks and Liars",
    "hillreporter_com": "Hill Reporter",
    "theintercept_com": "The Intercept",
    "jacobin_com": "Jacobin",
    "americanindependent_com": "The American Independent",
    "scrippsnews_com": "Scripps News",
    "www_ft_com": "Financial Times",
    "www_thefiscaltimes_com": "The Fiscal Times",
    "thegrio_com": "The Grio",
    "dallasnews_com": "The Dallas Morning News",
    "thepeoplesvoice_tv": "The People's Voice",
    "www_palmerreport_com": "Palmer Report",
    "bostonherald_com": "Boston Herald",
    "cbn_com": "CBN",
    "pjmedia_com": "PJ Media",
    "www_foxnews_com_shows_the_five": "The Five",
    "www_cbs_com_shows_60_minutes": "60 Minutes",
    "www_foxnews_com_shows_journal_editorial_report": "Journal Editorial Report",
    "www_infowars_com_show_the_alex_jones_show": "The Alex Jones Show",
    "www_forbes_com": "Forbes",
    "fortune_com": "Fortune",
    "freebeacon_com": "Washington Free Beacon",
    "www_washingtontimes_com": "The Washington Times",
    "www_wonkette_com": "Wonkette",
    "www_wnd_com": "WorldNetDaily",
    "forward_com": "The Forward",
    "theepochtimes_com": "The Epoch Times",
    "advocate_com": "The Advocate",
    "christianitytoday_com": "Christianity Today",
    "www_independent_co_uk_us": "The Independent",
    "westernjournal_com": "The Western Journal",
    "rawstory_com": "Raw Story",
    "vogue_com": "Vogue",
    "mediaite_com": "Mediaite",
    "airforcetimes_com": "Air Force Times",
    "glennbeck_com": "Glenn Beck",
    "freep_com": "Detroit Free Press",
    "bnonews_com": "BNO News",
    "theverge_com": "The Verge",
    "newser_com": "Newser",
    "rightwingwatch_org": "Right Wing Watch",
    "news_sky_com": "Sky News",
    "www_mirror_co_uk": "The Mirror",
    "11alive_com": "11Alive",
    "foxbusiness_com": "Fox Business",
    "justthenews_com": "Just the News",
    "thecollegefix_com": "The College Fix",
    "www_afp_com_en": "AFP",
    "barrons_com": "Barron's",
    "foreignaffairs_com": "Foreign Affairs",
    "cnet_com": "CNET",
    "thegrayzone_com": "The Grayzone",
    "newsnationnow_com": "NewsNation",
    "cosmopolitan_com": "Cosmopolitan",
    "upworthy_com": "Upworthy",
    "politifact_com": "PolitiFact",
    "thespectator_com": "The Spectator",
    "nysun_com": "The New York Sun",
    "theglobeandmail_com": "The Globe and Mail",
    "ncregister_com": "National Catholic Register",
    "christianpost_com": "The Christian Post",
    "rebelnews_com": "Rebel News",
    "newstarget_com": "NewsTarget",
    "nowthisnews_com": "NowThis News",
    "socialistalternative_org": "Socialist Alternative",
    "publishedreporter_com": "The Published Reporter",
    "themarshallproject_org": "The Marshall Project",
    "www_levernews_com": "The Lever",
    "thedispatch_com_podcast_dispatch_podcast": "The Dispatch Podcast",
    "thepostmillennial_com": "The Post Millennial",
    "crooked_com_podcast_series_pod_save_america": "Pod Save America",
    "www_dailywire_com_show_the_ben_shapiro_show": "The Ben Shapiro Show",
    "www_nytimes_com_column_the_daily": "The Daily",
    "charliekirk_com_podcasts": "Charlie Kirk",
    "fivethirtyeight_com_tag_politics_podcast": "FiveThirtyEight Politics Podcast",
    "bongino_com_podcasts": "The Dan Bongino Show",
    "www_npr_org_podcasts_510318_up_first": "Up First",
    "www_marklevinshow_com": "Mark Levin Show",
    "www_devilmaycaremedia_com_megynkellyshow": "The Megyn Kelly Show",
    "louderwithcrowder_com": "Louder with Crowder",
    "www_npr_org_podcasts_500005_npr_news_now": "NPR News Now",
    "www_wsj_com_podcasts_the_journal": "The Journal",
    "www_smartless_com_episodes": "SmartLess",
    "www_npr_org_podcasts_510312_codeswitch": "Code Switch",
    "podcasts_apple_com_us_podcast_the_rubin_report_id1052842770": "The Rubin Report",
    "podcast_thebulwark_com": "The Bulwark Podcast",
    "soundcloud_com_chapo_trap_house": "Chapo Trap House",
    "jimmydorecomedy_com": "The Jimmy Dore Show",
    "www_wsj_com_podcasts_opinion_potomac_watch": "Potomac Watch",
    "www_michaelmoore_com_archive": "Rumble with Michael Moore",
    "hartmannreport_com": "The Hartmann Report",
    "blavity_com": "Blavity",
    "americanactionforum_org": "American Action Forum",
    "www_foxbusiness_com_shows_the_claman_countdown": "The Claman Countdown",
    "www_foxnews_com_shows_gutfeld": "Gutfeld!",
    "radio_foxnews_com_podcast_will_cain_podcast": "The Will Cain Podcast",
    "wng_org": "WORLD News Group",
    "www_oann_com_schedule": "OANN Schedule",
    "www_newsnationnow_com_danabramslive": "Dan Abrams Live",
    "nutritruth_org": "NutriTruth",
    "www_foxnews_com_shows_jesse_watters_primetime": "Jesse Watters Primetime",
    "san_com": "San Diego Union-Tribune",
    "www_thedailybeast_com_franchise_the_new_abnormal": "The New Abnormal",
    "allinchamathjason_libsyn_com_website": "All-In Podcast",
    "www_foxnews_com_shows_fox_news_sunday": "Fox News Sunday",
    "pod_link_1561049560": "Unknown Podcast",
    "timcast_com_channel_timcast_irl": "Timcast IRL",
    "www_pbs_org_show_newshour": "PBS NewsHour",
    "politizoom_com": "PolitiZoom",
    "www_msnbc_com_jen_psaki": "Jen Psaki Show",
    "scrippsnews_com_series_early_rush": "Scripps Early Rush",
    "usafacts_org": "USA Facts"
}

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto("https://adfontesmedia.com/interactive-media-bias-chart/")
        
        await page.wait_for_selector('iframe.iframeChart')

        iframe_element = await page.query_selector('iframe.iframeChart')
        iframe = await iframe_element.content_frame()
        
        await iframe.wait_for_selector('g.zoomableArea')
        
        reliability_dict = {}
        
        images_info = await iframe.evaluate('''
            () => {
                const images = document.querySelectorAll('g.zoomableArea image');
                return Array.from(images).map(img => ({
                    name: img.getAttribute('href').split('/').pop().split('.').shift(),
                    y: img.getAttribute('y')
                }));
            }
        ''')

        for img in images_info:
            url_name = img['name']
            y_position = float(img['y'])
            reliability_score = (y_position - 495) / -9.2985318108 + 12.33
            actual_name = name_mapping.get(url_name, url_name)
            reliability_dict[actual_name] = reliability_score
            print(actual_name)

        with open('adFontesMediaReliabilityRatings.json', 'w') as f:
            json.dump(reliability_dict, f, indent=4)
        
        await browser.close()

asyncio.run(main())
