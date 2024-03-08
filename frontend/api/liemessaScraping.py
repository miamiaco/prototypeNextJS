import requests
from bs4 import BeautifulSoup
import json
import re

# List of recipe URLs
recipe_urls = [
    "https://liemessa.fi/2021/02/hapanjuurileivonta/",
    "https://liemessa.fi/2018/05/piknik-brunssi/",
    "https://liemessa.fi/2018/08/taydellisen-kalan-paistaminen-8-vinkkia/",
    "https://liemessa.fi/2016/12/diy-viininmaistajaiset/",
    "https://liemessa.fi/2018/08/kesakurpitsalasagne/",
    "https://liemessa.fi/2017/06/lakritsipannukakut/",
    "https://liemessa.fi/2022/10/kurpitsapasta-2/",
    "https://liemessa.fi/2017/09/kanttarellikvinoa/",
    "https://liemessa.fi/2016/09/mifu-shakshuka/",
    "https://liemessa.fi/2017/08/ruisletut-mascarponevaahdolla/",
    "https://liemessa.fi/2017/07/kyro-distillery-company/",
    "https://liemessa.fi/2011/09/suppilovahvero-perunapiirakka/",
    "https://liemessa.fi/2021/08/kreikkalainen-hunajakakku/",
    "https://liemessa.fi/2006/11/oranssi-keitto/",
    "https://liemessa.fi/2020/02/tomaattipestopasta-lidl-suosikki/",
    "https://liemessa.fi/2012/08/uunipunajuuret/",
    "https://liemessa.fi/2022/04/pikkeloidyt-tomaatit/",
    "https://liemessa.fi/2011/02/kesakurpitsapasta-kylpee-salaman-paisteessa/",
    "https://liemessa.fi/2022/06/tiramisukakku-mansikoilla/",
    "https://liemessa.fi/2008/10/chili-papukeitto/",
    "https://liemessa.fi/2017/09/teriyaki-uunilohi/",
    "https://liemessa.fi/2019/05/parsarisotto/",
    "https://liemessa.fi/2021/08/luumupiirakka-ja-hyggekauden-avajaiset/",
    "https://liemessa.fi/2012/04/fetalla-taytetyt-paprikat/",
    "https://liemessa.fi/2021/01/spelttileipa-hapanjuureen/",
    "https://liemessa.fi/2021/03/cacio-e-pepe-eli-mustapippuripasta/",
    "https://liemessa.fi/2022/02/geishapalat/",
    "https://liemessa.fi/2019/03/parsapiilot/",
    "https://liemessa.fi/2017/11/viikunakakku/",
    "https://liemessa.fi/2016/04/jogurttijaatelo/",
    "https://liemessa.fi/2012/09/munakoisopasta/",
    "https://liemessa.fi/2020/10/aurakaalilaatikko/",
    "https://liemessa.fi/2018/10/simpukkapasta/",
    "https://liemessa.fi/2018/08/kukkakaaliwingsit/",
    "https://liemessa.fi/2020/08/maissintahkat-ras-el-hanout/",
    "https://liemessa.fi/2010/10/oon-ma-syony-lehmaa-viinissa/",
    "https://liemessa.fi/2017/08/kesakurpitsatalkoot/",
    "https://liemessa.fi/2017/10/mustatorvisienipasta/",
    "https://liemessa.fi/2010/11/mamman-lihapullat/",
    "https://liemessa.fi/2017/02/vegebrunssi/",
    "https://liemessa.fi/2018/03/brunssikirja-julkkarit/",
    "https://liemessa.fi/2020/02/kotivaralista/",
    "https://liemessa.fi/2019/08/harkislasagne-uunitomaateilla/",
    "https://liemessa.fi/2013/10/pasta-carbonara-hyvaa-20-minuutissa/",
    "https://liemessa.fi/2022/10/korvapuustipelti/",
    "https://liemessa.fi/2017/06/kirsikkasmoothie/",
    "https://liemessa.fi/2014/02/kesakurpitsalasagne-ja-poydan-putsaus/",
    "https://liemessa.fi/2022/09/harissa-orzotto/",
    "https://liemessa.fi/2012/08/lasagne-kuudella-tapaa/",
    "https://liemessa.fi/2020/09/sadonkorjuupiirakka/",
    "https://liemessa.fi/2019/05/pellolta-poytaan-uunipalsternakka/",
    "https://liemessa.fi/2019/06/munakoisolasagne/",
    "https://liemessa.fi/2017/04/kevatsalaatti/",
    "https://liemessa.fi/2017/08/linssicurry/",
    "https://liemessa.fi/2019/03/vadelma-kinuski-vohvelikakku/",
    "https://liemessa.fi/2008/07/ainahan-se-on-mielessa-italia/",
    "https://liemessa.fi/2017/05/chilipasta/",
    "https://liemessa.fi/2020/01/uunipersimonit/",
    "https://liemessa.fi/2008/03/dagen-efter-pasken/",
    "https://liemessa.fi/2018/05/kesapiknik-seurasaareen/",
    "https://liemessa.fi/2022/02/korealainen-nuudelikeitto/",
    "https://liemessa.fi/2016/05/24h-ilman-lisaaineita/",
    "https://liemessa.fi/2021/12/paras-saaristolaisleipa/",
    "https://liemessa.fi/2020/05/mansikka-bruschetta-ja-mozzerellavartaat/",
    "https://liemessa.fi/2021/06/mansikka-mojito-mocktail-mysoda-hiilihapotuslaite/",
    "https://liemessa.fi/2012/08/maanantaisafkaa/",
    "https://liemessa.fi/2007/01/makaronilaatikko/",
    "https://liemessa.fi/2023/06/feta-perunanyytit-ja-halloumin-grillaus/",
    "https://liemessa.fi/2023/01/salviapestopasta/",
    "https://liemessa.fi/2020/08/perunamunakas-savulohella-ja-fetalla/",
    "https://liemessa.fi/2013/01/jauhelihakastike/",
    "https://liemessa.fi/2018/09/sieni-lohipata/",
    "https://liemessa.fi/2014/09/texmex-lehtikaali-munakas/",
    "https://liemessa.fi/2020/09/salt-vinegar-perunat-ja-maustamisen-abc/",
    "https://liemessa.fi/2021/04/vappu-platter-ja-dipit/",
    "https://liemessa.fi/2017/03/panopasta/",
    "https://liemessa.fi/2010/12/smetanalohi-ja-after-eight-kaurakeksit/",
    "https://liemessa.fi/2018/08/aasialainen-lohiwokki/",
    "https://liemessa.fi/2021/03/itsetehty-minttuhyytelo/",
    "https://liemessa.fi/2021/05/sahramipasta-simpukoilla/",
    "https://liemessa.fi/2011/05/paras-kotiruoka/",
    "https://liemessa.fi/2016/05/asennebrunssi/",
    "https://liemessa.fi/2017/02/uunilohi-ja-arkikattaus/",
    "https://liemessa.fi/2018/07/okra-uusi-tuttavuus/",
    "https://liemessa.fi/2018/03/taydellinen-pizza-pizzagoals/",
    "https://liemessa.fi/2019/03/pinaatti-lohilasagne/",
    "https://liemessa.fi/2021/09/bataattiveneet-mustapaputaytteella/",
    "https://liemessa.fi/2019/12/jouluvuoka/",
    "https://liemessa.fi/2016/05/tolkuttoman-viikon-ruokalista/",
    "https://liemessa.fi/2018/12/itsetehty-ruokalahja/",
    "https://liemessa.fi/2006/12/ruohosipuliriisi-ja-uunikana/",
    "https://liemessa.fi/2006/12/veemainen-kana/",
    "https://liemessa.fi/2008/01/upgreidattu-pasta-el-pesto/",
    "https://liemessa.fi/2019/02/uunifetapasta/",
    "https://liemessa.fi/2020/04/kevainen-brunssi-kotona/",
    "https://liemessa.fi/2010/04/cortsun-carbonara/",
    "https://liemessa.fi/2018/10/syksyinen-juustopoyta/",
    "https://liemessa.fi/2018/04/intialainen-mangolassi/",
    "https://liemessa.fi/2021/10/halloumipasta/",
    "https://liemessa.fi/2007/12/italialainen-sika-teki-temput/",
    "https://liemessa.fi/2016/04/broccoliinit-aasialaisittain/",
    "https://liemessa.fi/2020/03/kikherne-wrapit/",
    "https://liemessa.fi/2009/11/wagnerin-paras-pastakastike/",
    "https://liemessa.fi/2006/12/fusillia-sitruunapestolla/",
    "https://liemessa.fi/2007/03/tortellinit-tomaattikastikkeella/",
    "https://liemessa.fi/2017/04/churro-vohvelit/",
    "https://liemessa.fi/2007/01/vuohenjuustopasta/",
    "https://liemessa.fi/2023/02/hernehummus-ja-taydellinen-keitetty-kananmuna/",
    "https://liemessa.fi/2017/04/pretzelit-ja-juustodippi/",
    "https://liemessa.fi/2022/11/kreikkalainen-uunifeta/",
    "https://liemessa.fi/2020/10/hunajakanapelti/",
    "https://liemessa.fi/2020/07/punaviinimarjapiirakka/",
    "https://liemessa.fi/2020/03/kotivararuokaa-porkkanalasagne/",
    "https://liemessa.fi/2018/05/espanjalainen-peruna-kanapata/",
    "https://liemessa.fi/2022/08/kantarellikastike-mesjuustolla/",
    "https://liemessa.fi/2022/10/kurpitsafocaccia/",
    "https://liemessa.fi/2017/04/aasialainen-nuudelisalaatti/",
    "https://liemessa.fi/2017/01/asennekakkukahvit-kilpailu/",
    "https://liemessa.fi/2007/01/vihrea-keitto/",
    "https://liemessa.fi/2019/08/beanit-flatbread/",
    "https://liemessa.fi/2017/02/harkis-vihikset/",
    "https://liemessa.fi/2018/09/kasvisragu-ja-nain-puolitin-perheen-lihansyonnin/",
    "https://liemessa.fi/2007/01/kalapuikot-ja-perunamuusi/",
    "https://liemessa.fi/2012/12/soyappetit-soijakoulu-jouluinen-soijamureke/",
    "https://liemessa.fi/2020/02/harkispyorykkavuoka/",
    "https://liemessa.fi/2011/01/fashonperunat/",
    "https://liemessa.fi/2009/01/paras-pasta-2008/",
    "https://liemessa.fi/2017/03/tolkkitomaattikeitto/",
    "https://liemessa.fi/2022/01/turkkilainen-cilbir-uppomunaleipa/",
    "https://liemessa.fi/2017/09/chiavanukas/",
    "https://liemessa.fi/2015/09/puolukkasmoothie/",
    "https://liemessa.fi/2018/04/kurkumamunakas/",
    "https://liemessa.fi/2009/02/kolme-pienta-ruokaa-ystavalle/",
    "https://liemessa.fi/2019/04/vasterbottensost-pizza/",
    "https://liemessa.fi/2021/02/gouda-perunakeitto/",
    "https://liemessa.fi/2017/02/suklaapuuro/",
    "https://liemessa.fi/2019/01/verigreippisalaatti-kaikilla-sorsseleilla/",
    "https://liemessa.fi/2013/07/lempiaamiainen-jugurttiherkku/",
    "https://liemessa.fi/2018/02/talvinen-brunssi/",
    "https://liemessa.fi/2012/04/soyappetit-soijakoulu-osa-3-soijasuikaleet/",
    "https://liemessa.fi/2019/12/shortcakes-eli-skonssit/",
    "https://liemessa.fi/2021/01/talvinen-perunasalaatti/",
    "https://liemessa.fi/2019/02/punajuuririsotto/",
    "https://liemessa.fi/2007/10/lasagne-heittaa-voltin-ja-laskeutuu-jaloilleen/",
    "https://liemessa.fi/2021/04/hummuspasta/",
    "https://liemessa.fi/2019/05/lohikaaretorttu/",
    "https://liemessa.fi/2008/04/liha-herneenpalko-pasta/",
    "https://liemessa.fi/2018/10/3-x-unelmaleipa/",
    "https://liemessa.fi/2018/02/miten-saada-lapsi-syomaan-kasviksia/",
    "https://liemessa.fi/2019/06/ahvenanmaan-pannukakku/",
    "https://liemessa.fi/2019/09/uunitomaatti-flatbread/",
    "https://liemessa.fi/2015/11/isanpaiva-aamiainen/",
    "https://liemessa.fi/2020/10/hernepestopasta/",
    "https://liemessa.fi/2009/11/yrttiset-lammaspihvit/",
    "https://liemessa.fi/2019/09/puolukka-kinuskipiirakka/",
    "https://liemessa.fi/2018/01/pahkinainen-myslipaistos/",
    "https://liemessa.fi/2020/03/kaurapannukakut/",
    "https://liemessa.fi/2018/03/brunssikirja/",
    "https://liemessa.fi/2017/01/hernerisotto/",
    "https://liemessa.fi/2022/01/ndujapasta/",
    "https://liemessa.fi/2021/01/karamellisoitu-sipulipasta/",
    "https://liemessa.fi/2013/05/pastan-keittaminen-ja-pancetta-pasta-al-pomodoro-di-nirso/",
    "https://liemessa.fi/2018/10/kurpitsajuustokakku/",
    "https://liemessa.fi/2016/02/one-pot-kasvis-tofunuudelit/",
    "https://liemessa.fi/2021/12/roomalainen-levypizza-al-taglio/",
    "https://liemessa.fi/2021/12/piparijuustokakku/",
    "https://liemessa.fi/2020/12/pinaatti-fetapasta/",
    "https://liemessa.fi/2016/09/kulhoruoka-chili-con-carne-2/",
    "https://liemessa.fi/2020/01/minttupestopasta/",
    "https://liemessa.fi/2020/11/suklaiset-tahinikeksit/",
    "https://liemessa.fi/2021/04/parsaleivat-hollandaisekastike-ja-kevattuulia/",
    "https://liemessa.fi/2018/10/lohikulho/",
    "https://liemessa.fi/2007/08/wienerleike-on-oikeaa-ruokaa/",
    "https://liemessa.fi/2016/02/mummun-siskonmakkarakeitto/",
    "https://liemessa.fi/2022/05/kyproslaiset-halloumiranskalaiset/",
    "https://liemessa.fi/2018/04/granaattiomenasima/",
    "https://liemessa.fi/2007/09/saint-agur-ja-pimean-energian-arvoitus/",
    "https://liemessa.fi/2017/06/juustopaprikat/",
    "https://liemessa.fi/2009/09/lammas-ricotta-lasagne/",
    "https://liemessa.fi/2019/04/lohipelti/",
    "https://liemessa.fi/2019/03/paahdetut-paprika-crostinit/",
    "https://liemessa.fi/2009/01/paras-keittokirja-2008/",
    "https://liemessa.fi/2023/09/halloumilasagne/",
    "https://liemessa.fi/2017/01/harissa-bataattikeitto/",
    "https://liemessa.fi/2021/10/uunifetaperunat/",
    "https://liemessa.fi/2014/08/valkosipulin-ja-sitruunan-makuinen-syksy/",
    "https://liemessa.fi/2013/03/soija-kikherne-pasta/",
    "https://liemessa.fi/2011/10/pancotto-italialainen-tomaattikeitto-2/",
    "https://liemessa.fi/2007/01/liha-papu-pata/",
    "https://liemessa.fi/2017/06/raparperipaistos/",
    "https://liemessa.fi/2017/02/liila-bataattitoast/",
    "https://liemessa.fi/2009/04/chilia-lihalla/",
    "https://liemessa.fi/2020/08/italialainen-munakoisovuoka/",
    "https://liemessa.fi/2022/08/kreikkalaiset-paahdetut-munakoisot/",
    "https://liemessa.fi/2008/05/vain-vakiintuneille-kaalilaatikko/",
    "https://liemessa.fi/2016/09/sunnuntaibrunssi/",
    "https://liemessa.fi/2006/12/pekoni-parsakaali-pasta/",
    "https://liemessa.fi/2021/12/puolukkababka/",
    "https://liemessa.fi/2019/02/savulohipasta-x-2/",
    "https://liemessa.fi/2012/08/punajuuri-tarte-tatin/",
    "https://liemessa.fi/2017/01/tofukulho-taydellisen-tofun-salaisuus/",
    "https://liemessa.fi/2017/11/aasialaiset-lihapullat/",
    "https://liemessa.fi/2018/01/uunijuures-linssisalaatti/",
    "https://liemessa.fi/2019/08/rapujuhlien-menu/",
    "https://liemessa.fi/2009/01/kg-mureke/",
    "https://liemessa.fi/2021/02/peruna-kaalilaatikko/",
    "https://liemessa.fi/2020/11/parmesaani-perunavohvelit/",
    "https://liemessa.fi/2020/09/kaalipasta-ja-mukulaselleri-uunissa/",
    "https://liemessa.fi/2019/10/tuparibrunssi/",
    "https://liemessa.fi/2014/01/mutti-soosi/",
    "https://liemessa.fi/2019/06/harkapapuhampurilainen/",
    "https://liemessa.fi/2020/10/kurpitsavuoka/",
    "https://liemessa.fi/2018/09/chili-con-carne/",
    "https://liemessa.fi/2020/08/punajuuriletut/",
    "https://liemessa.fi/2011/02/penninvenyttajan-kaalilaatikko/",
    "https://liemessa.fi/2020/12/mallasleipa-ja-juustotarjottimen-kokoaminen/",
    "https://liemessa.fi/2013/09/pinaattiletut/",
    "https://liemessa.fi/2022/01/tahinilaskiaispullat/",
    "https://liemessa.fi/2015/10/kurpitsapiirakka-aamupalaksi/",
    "https://liemessa.fi/2020/06/beanit-grillinyytit/",
    "https://liemessa.fi/2007/01/seitikeitto/",
    "https://liemessa.fi/2018/01/veriappelsiinirisotto/",
    "https://liemessa.fi/2013/10/kurpitsakeitto/",
    "https://liemessa.fi/2021/03/itse-tehty-tuorepasta/",
    "https://liemessa.fi/2014/03/kevatpizza-spelttipizzapohjaan/",
    "https://liemessa.fi/2017/03/mifu-laksa/",
    "https://liemessa.fi/2016/01/sardiinipasta-ja-muutoksen-tuulet/",
    "https://liemessa.fi/2019/04/helsingin-paras-brunssi-lapland-hotels-bulevardi/",
    "https://liemessa.fi/2013/06/soija-nuudeli-salaatti/",
    "https://liemessa.fi/2017/03/suklaavohvelit/",
    "https://liemessa.fi/2020/10/mezepoyta-falafel/",
    "https://liemessa.fi/2018/02/kookoscurry-lihapullat/",
    "https://liemessa.fi/2012/10/wildfood-villeja-resepteja/",
    "https://liemessa.fi/2021/04/kierremunkit/",
    "https://liemessa.fi/2021/11/kreikkalainen-linssikeitto/",
    "https://liemessa.fi/2009/03/simppeli-uunilohi/",
    "https://liemessa.fi/2020/09/manteli-omenapiirakka/",
    "https://liemessa.fi/2017/09/brunssikirja-brunch-all-day/",
    "https://liemessa.fi/2016/10/talvisalaatti-ja-hernekastike/",
    "https://liemessa.fi/2021/09/hapankaalipasta/",
    "https://liemessa.fi/2021/05/nokkosen-kuivaaminen-ja-nokkosjauhe/",
    "https://liemessa.fi/2010/01/lindstromin-piffit/",
    "https://liemessa.fi/2022/08/seesamitofu/",
    "https://liemessa.fi/2012/03/kevainen-tuulahdus-lahi-idasta/",
    "https://liemessa.fi/2018/04/raikas-vadelma-vuohenjuustosalaatti/",
    "https://liemessa.fi/2015/10/omenaiset-homejuustoperunat/",
    "https://liemessa.fi/2013/02/remoulade-kastike-ja-taytetty-bagel/",
    "https://liemessa.fi/2006/12/ceasar-salaatti/",
    "https://liemessa.fi/2020/01/harkis-kaalilaatikko/",
    "https://liemessa.fi/2014/04/kermainen-parsapasta/",
    "https://liemessa.fi/2018/01/paistettu-riisi-kikherneilla/",
    "https://liemessa.fi/2020/04/storyn-itsetehty-granola/",
    "https://liemessa.fi/2019/06/nokkosvohvelit/",
    "https://liemessa.fi/2013/05/banaaniletut/",
    "https://liemessa.fi/2021/05/tahini-banaanileipa/",
    "https://liemessa.fi/2020/12/matkavinkit-ivalo-rovaniemi/",
    "https://liemessa.fi/2018/02/ystavanpaiva-brunssi/",
    "https://liemessa.fi/2021/02/ystavanpaivan-pinkki-pasta/",
    "https://liemessa.fi/2018/09/halloumitacot/",
    "https://liemessa.fi/2011/01/suomalainen-sipulikeitto/",
    "https://liemessa.fi/2018/07/kirsikka-suklaa-vohvelikakku/",
    "https://liemessa.fi/2017/12/joululaatikot-ja-perinteet-uusiksi/",
    "https://liemessa.fi/2019/08/sarkipasta/",
    "https://liemessa.fi/2015/09/omena-kaneli-tuorepuuro/",
    "https://liemessa.fi/2020/12/pentikin-uskomaton-tarina/",
    "https://liemessa.fi/2017/08/mummonkurkut/",
    "https://liemessa.fi/2021/10/savuinen-suppilovahveropiirakka/",
    "https://liemessa.fi/2019/10/ananaslampparit/",
    "https://liemessa.fi/2024/02/munakoisopasta-2/",
    "https://liemessa.fi/2022/05/lohipelti-ras-el-hanout/",
    "https://liemessa.fi/2020/11/ginipasta/",
    "https://liemessa.fi/2018/03/kevainen-juustotarjotin/",
    "https://liemessa.fi/2018/09/homejuusto-omenagalette/",
    "https://liemessa.fi/2017/01/banaanileipa/",
    "https://liemessa.fi/2014/10/helppo-sitruuna-valkosipuli-pasta/",
    "https://liemessa.fi/2009/05/homeservice-palveluksessanne/",
    "https://liemessa.fi/2014/04/churrot-ja-suklaakastike/",
    "https://liemessa.fi/2016/08/puolukka-mocktail/",
    "https://liemessa.fi/2016/11/lihapullavuoka-ja-testissa-miele-astianpesukone/",
    "https://liemessa.fi/2018/03/brunssimuffinssit/",
    "https://liemessa.fi/2018/06/kesamenu-valio-x-gron/",
    "https://liemessa.fi/2021/05/kreikkalainen-katkarapupannu/",
    "https://liemessa.fi/2020/05/batata-harra-eli-tuliset-perunat-ja-inkivaarilohi/",
    "https://liemessa.fi/2020/05/beanit-pasta-carbonara/",
    "https://liemessa.fi/2019/03/natuviinit-ja-korealaiset-kimchinuudelit/",
    "https://liemessa.fi/2014/10/keittion-kunkut-ja-sriratsa-nuudelit/",
    "https://liemessa.fi/2023/04/pil-pil-pasta/",
    "https://liemessa.fi/2019/09/oreo-suklaavohvelit/",
    "https://liemessa.fi/2019/06/mokkiruokaa-harkis-sandwich/",
    "https://liemessa.fi/2021/08/uunimuikut-ja-puolukkamajoneesi/",
    "https://liemessa.fi/2020/04/pirtea-vappubrunssi/",
    "https://liemessa.fi/2019/10/uunifetaraviolit/",
    "https://liemessa.fi/2007/12/aitien-tekemaa-ruokaa-siskonmakkarakeitto/",
    "https://liemessa.fi/2007/09/rasvapommista-mustaan-aukkoon/",
    "https://liemessa.fi/2017/08/kesakurpitsaspagetti/",
    "https://liemessa.fi/2018/07/grillattu-polentakakku/",
    "https://liemessa.fi/2018/02/kalakeittopaiva/",
    "https://liemessa.fi/2020/06/miten-saada-lapsi-syomaan-terveellisesti/",
    "https://liemessa.fi/2022/03/kimchi-pannukakut/",
    "https://liemessa.fi/2020/08/maisemakahvilan-raparperipiirakka/",
    "https://liemessa.fi/2011/10/uuniperuna-riittoisa-arkiruoka/",
    "https://liemessa.fi/2020/04/uunifetaparsa/",
    "https://liemessa.fi/2013/05/frittata-italialainen-munakas/",
    "https://liemessa.fi/2017/11/homejuusto-punajuurikeitto/",
    "https://liemessa.fi/2016/01/uunipeltimakaronilaatikko/",
    "https://liemessa.fi/2020/08/paahdettu-kukkakaalikeitto/",
    "https://liemessa.fi/2021/10/srirachapasta/",
    "https://liemessa.fi/2012/02/makaronilaatikko-ja-muita-arjen-pelastajia/",
    "https://liemessa.fi/2017/08/kukkakaalitalkoot/",
    "https://liemessa.fi/2018/04/parsafocaccia/",
    "https://liemessa.fi/2007/03/miljonaari-jussin-klasarikana-tvsta-tuttu/",
    "https://liemessa.fi/2012/03/soyappetit-soijakoulu-osa-2-soijalasagne/",
    "https://liemessa.fi/2019/09/beanit-vihrea-curry/",
    "https://liemessa.fi/2018/04/sitruunarisotto/",
    "https://liemessa.fi/2022/05/vegaaninen-raparperipiirakka-ja-jaakahvi/",
    "https://liemessa.fi/2020/03/mustikkakakku/",
    "https://liemessa.fi/2007/07/9-barin-pollo-limonello-muistaakseni/",
    "https://liemessa.fi/2016/02/avokadoleipa-uppomunalla/",
    "https://liemessa.fi/2018/05/mantelitaytekakku/",
    "https://liemessa.fi/2020/08/sienitortellinit/",
    "https://liemessa.fi/2010/01/punajuuri-kaalilaatikko/",
    "https://liemessa.fi/2016/06/gluteeniton-brunssi/",
    "https://liemessa.fi/2020/05/hapanjuuren-valmistaminen/",
    "https://liemessa.fi/2020/08/kasvispelti-vuohenjuustolla-ja-lohella/",
    "https://liemessa.fi/2020/04/bataatticurry/",
    "https://liemessa.fi/2012/09/soyappetit-soijakoulu-penninvenyttajan-soijaresepti/",
    "https://liemessa.fi/2019/06/uuniraparperihillo/",
    "https://liemessa.fi/2018/07/chili-aprikoosihillo/",
    "https://liemessa.fi/2017/05/aitienpaivan-aamiainen/",
    "https://liemessa.fi/2017/09/satay-mifu-suikaleet/",
    "https://liemessa.fi/2018/06/kirsikkapizza/",
    "https://liemessa.fi/2008/04/herneet-nenassa/",
    "https://liemessa.fi/2017/10/kurpitsapannukakut/",
    "https://liemessa.fi/2020/06/kesakurpitsavuoka/",
    "https://liemessa.fi/2017/06/munakoisopita/",
    "https://liemessa.fi/2011/01/viikon-kasvisruoka-tomaatti-papusoppa/",
    "https://liemessa.fi/2019/11/aito-italialainen-ragu-alla-bolognese/",
    "https://liemessa.fi/2020/05/suklaacroissantit/",
    "https://liemessa.fi/2019/11/kookos-kurpitsakeitto/",
    "https://liemessa.fi/2017/06/skagenrora-katkaraputahna/",
    "https://liemessa.fi/2022/04/kreikkalainen-perunasalaatti/",
    "https://liemessa.fi/2018/09/maapahkinavoipuuro/",
    "https://liemessa.fi/2007/08/puputin-munakokkeli/",
    "https://liemessa.fi/2014/05/lammaslihapullat-amatoorikokin-kotiruokaa/",
    "https://liemessa.fi/2019/01/sitruunapasta/",
    "https://liemessa.fi/2012/04/parsan-keittaminen/",
    "https://liemessa.fi/2020/05/aitienpaivan-brunssi/",
    "https://liemessa.fi/2020/08/helppo-kinuskinen-omenapiirakka/",
    "https://liemessa.fi/2017/03/tortillapizza/",
    "https://liemessa.fi/2020/09/baked-feta-pasta-original-recipe/",
    "https://liemessa.fi/2021/03/sitruuna-vadelma-vohvelikakku/",
    "https://liemessa.fi/2019/03/uunifetamunakas/",
    "https://liemessa.fi/2020/03/kikherne-limonello/",
    "https://liemessa.fi/2016/11/hatsapuri/",
    "https://liemessa.fi/2015/11/meksikolainen-brunssi-huevos-rancheros/",
    "https://liemessa.fi/2018/04/linssibolognese/",
    "https://liemessa.fi/2021/08/kesakurpitsa-halloumipihvit/",
    "https://liemessa.fi/2008/08/pataa-futaajille/",
    "https://liemessa.fi/2019/02/kukkakaalicurry/",
    "https://liemessa.fi/2021/09/kurpitsarisotto/",
    "https://liemessa.fi/2015/11/arkiruoka-x-3/",
    "https://liemessa.fi/2018/05/sydamelliset-raparperileivokset/",
    "https://liemessa.fi/2018/06/italialainen-antipasto/",
    "https://liemessa.fi/2016/09/uunipaarynat/",
    "https://liemessa.fi/2022/08/halloumipelti/",
    "https://liemessa.fi/2021/08/tomaattirisotto/",
    "https://liemessa.fi/2019/02/kasviskaalikaaryleet-pannulla/",
    "https://liemessa.fi/2017/12/riisipuuro-x-3/",
    "https://liemessa.fi/2018/01/taytetyt-pinaattiletut/",
    "https://liemessa.fi/2017/05/korianterimunakas/",
    "https://liemessa.fi/2016/04/kokonainen-thai-siika/",
    "https://liemessa.fi/2023/10/pasta-et-fagioli-eli-papupasta/",
    "https://liemessa.fi/2023/02/maapahkinavoicurry/",
    "https://liemessa.fi/2007/08/pipe-rigate-alle-lammas-ricotta/",
  #  "https://liemessa.fi/2012/05/brunssi-menu/",
    "https://liemessa.fi/2016/04/instagram-hinkkausta-ja-arkiruokahaaste/",
    "https://liemessa.fi/2016/02/nakkikastike-ja-kolmas-lapsi/",
    "https://liemessa.fi/2016/02/uuniveriappelsiinit/",
    "https://liemessa.fi/2012/08/kanttarellikastike/",
    "https://liemessa.fi/2021/04/kukkakaalitacot/",
    "https://liemessa.fi/2006/12/lohta-ja-herkkusienia-pestokastikkeessa/",
    "https://liemessa.fi/2006/11/paaryna-homejuusto-salaatti/",
    "https://liemessa.fi/2021/12/piparimuffinssit-karpalokuorrutteella/",
    "https://liemessa.fi/2010/01/jenssonin-kiusaus/",
    "https://liemessa.fi/2020/05/nachopelti/",
    "https://liemessa.fi/2006/11/jonilaiset-lihapullat/",
    "https://liemessa.fi/2017/05/lisukkeet-grilliruoalle/",
    "https://liemessa.fi/2016/05/arkiruokaa-se-huokaa/",
    "https://liemessa.fi/2017/04/tacopurkki/",
    "https://liemessa.fi/2019/11/pasta-puttanesca/",
    "https://liemessa.fi/2017/04/meze-lautanen/",
    "https://liemessa.fi/2021/12/tahtijoulutorttu/",
    "https://liemessa.fi/2016/12/kasvispainotteinen-joulumenu/",
    "https://liemessa.fi/2018/12/leipakranssi/",
    "https://liemessa.fi/2013/08/kasvissosekeitto-paahdetuista-juureksista/",
    "https://liemessa.fi/2009/08/jaakaappidyykkarin-pasta/",
    "https://liemessa.fi/2021/12/koyhat-ritarit-luumurahkalla/",
    "https://liemessa.fi/2012/09/omenainen-pull-apart-pulla/",
    "https://liemessa.fi/2012/09/sienirisotto/",
    "https://liemessa.fi/2019/04/3-x-brunssileipa/",
    "https://liemessa.fi/2013/11/amerikkalaiset-vanilja-pannukakut/",
    "https://liemessa.fi/2020/11/karjalanpiirakat/",
    "https://liemessa.fi/2018/05/lohi-pesto-nakuvoileipakakku/"
]


def scrape_recipe(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Scrape the title of the recipe
    title_tag = soup.find('h1', class_='entry-title')
    title = title_tag.get_text(strip=True) if title_tag else 'No Title Found'
    
    # Find the <p> element that contains "Ohje"
    ohje_tag = soup.find('p', string=re.compile('ohje', re.IGNORECASE))
    
    # Initialize content storage
    content_elements = []
    
  # Find the <h2> element that matches the title
    h2_tag = soup.find('h2', string=title)
    
    if h2_tag:
        # Get all next siblings and filter by <p>, <ul>, and <ol> tags
        for sibling in h2_tag.find_next_siblings():
            if sibling.name in ['p', 'ul', 'ol']:
                content_elements.append(str(sibling))
            else:
                break  # Stop if the next sibling is not a <p>, <ul>, or <ol>
    else:
        print(f"No matching <h2> element found for title '{title}' in {url}")
    
    # Concatenate all elements into a single string
    all_content_html = "".join(content_elements)
    
    # Find the container <div> with class "entry-content single-content"
    content_div = soup.find('div', class_='entry-content single-content')
    
    # Initialize an empty list for image URLs
    image_urls = []
    
    # If the container is found
    if content_div:
        # Find all <img> elements with a class attribute within the container
        images = content_div.find_all('img', class_=lambda x: x and x.startswith('wp'))
        
        # Extract the 'src' attribute of each <img> tag
        image_urls = [img['src'] for img in images]

    
    return {
        'url': url,
        'title': title,
        'content': all_content_html,
        'images': image_urls  # Direct URLs of the images, excluding the specified one
    }

# List to store the content of each recipe
recipes_content = []

recipe_count = 0

# Iterate through URLs and scrape content, title, and images for each, excluding specific images
for url in recipe_urls:
    print(f"Scraping content from {url}")
    recipe_data = scrape_recipe(url)
    recipes_content.append(recipe_data)
    recipe_count += 1 

print(f"Total number of recipes scraped: {recipe_count}")

# Convert the list of recipe data to JSON
json_content = json.dumps(recipes_content, indent=4, ensure_ascii=False)

# Optionally, save the JSON to a file
with open('anninuunissa.json', 'w', encoding='utf-8') as f:
    f.write(json_content)
