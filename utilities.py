# =========================
# ==== Support file   =====
import re
import numpy as np
from nltk import ngrams


solar = ["ج", "ن", "ل", "ط", "ظ", "ض", "ص", "س", "ش", "ر", "ز", "د", "ذ", "ت", "ث"]

#words without etymological diphtongs
avoid = ['موتة', 'موس','بوسعادة', 'موش', 'موشي', 'لوبان', 'فورار', 'سوس', 'فوروم', 'آوك', 'كورة', 'جوغرافية', 'موتوتي', 'مومن', 'جوع ', 'فول', 'بوس', 'بوسة', 'تونسي', 'فوه', 'موه', 'مود', 'يوا', 'غوي','بوغلم', 'هوني', 'غول', 'قول', 'قوة', 'ووهههه', 'سوق', 'تونسي', 'كورة', 'سوء', 'نور', 'دودان', 'رومانسي', 'نومرو', 'نورمال', 'موسم', 'هوني','زوز', 'ثوم', 'بوقلب', 'ريحة', 'شيشة', 'بيدها', 'ميترو', 'ريڨل', 'شيرة','شيرتنا', 'تيتروات', 'بيعة', 'سيتيرنا', 'ريّة', 'كيلمترة', 'قيمات','ريماتي', 'ثيقتي', 'ريفي', 'بيران','ريق', 'ديمقراطية', 'قياد', 'ميام', 'نيب', 'ميزيريا', 'رياضي', 'ثيقة','ميزان', 'ميلاد', 'سينيما', 'بيلانتي', 'بيلانتيات', 'زينة', 'كيراتين', 'قياسك', 'دين', 'ميمتي', 'بيرا', 'كيلوميتر','دينار', 'بيبان', 'لين', 'كيسان', 'دياري', 'آيّة', 'فوسط', 'لواحد', 'بو خشم', 'كيلعباد', 'كينقل لك', 'ديرابي','إيمانك', 'بيرها', 'بيده', 'ريقك', 'دياركم', 'ليالي', 'ميلادك', 'بيدي', 'زينها', 'قوت',  'دوڨ', 'طوب', 'كورسي', 'بوليس', 'لوبية', 'موسيقى', 'بوشوشة', 'بوليسية', 'لوسي', 'مولة', 'مودرج', 'بونيتة', 'بوكلوات', 'قورأ', 'جوجوات', 'بوز', 'بونية', 'سوبية', 'حوت', 'موتو', 'كونجي', 'لود', 'لوطة', 'سورة', 'لواجات', 'لواج', 'بونبوك', 'طول', 'موتى', 'بونو', 'بولحية', 'كون', 'سوري', 'سورية', 'بوخثير', 'ووي', 'رومنسية', 'فور', 'توب', 'تونسية', 'توانسة', 'يوزّع', 'بوهالي', 'زورونا','ميش', 'قيمة', 'ميش حسّيت', 'سيسوات', 'سياسيات', 'سياسية', 'سياسة', 'سياسي', 'سيتزيت', 'دينك', 'شيخة', 'فوت',  'تونسنا', 'موش', 'تونسيّة', 'سيقوم', 'كيّننا', 'كيان', 'جوغرافيّة', 'هويّة', 'قوّة', 'بيزنطيّة', 'قياسيّة', 'بيّك']
p_avoid = ['CONJ+PRON_3MS', 'CONJ+IV3P',  '[PREP', 'CONJ+IV3MS', 'IV1S', 'IV2S', 'IV3MS', 'IV3FS', 'IV1P', 'IV2P', 'IV3P', 'PV', 'CV2S', 'CV2P', 'SUB_CONJ+PRON_3P', 'CONJ+PRON_2S', 'CONJ+PRON_2P', 'CONJ+DET', 'CONJ+POSS_PRON_3FS', 'CONJ+PRON_3P', 'CONJ+PRON_1S', 'CONJ+PRON_1P', 'CONJ+NOUN']
weak_verbs = ['يهديوا', 'يهدوا ', 'لقوا','يبدوا','ولّاوا','نخلّيوا','نحكيوا','نبداوا','اعطوا','يتوشيوا','نمشوا','نحكوا','قضاوا','عطاوا','عطوا','تنحيوا','يدريوا','اقراوا','نعدّوا','تهنيوا','يحكيوا','نحشيوا','يزّيوا','اجاوا','خلّوا','يستنّوا','ينحوا','ماشوا','تحكيوا','يخريوا','يعطيوا','يعطوا','نساوا','يمشوا','يورّيوا','يبداوا','يتعدّاوا','نقصّيوا','مشاوا','كلاوا','يناديوا','يتولّيوا','ننساوا','يسمّيوا','نجيوا','نبدوا','نقراوا','ينحّيوا','تصليوا','تدعيوا','نمشيوا','نتعدّاوا','يلقاوا','نقضيوا','نغنيوا','نحيوا','خلّيوا','تعطيوا','نجريوا','يستنّاوا','يمشيوا','بداوا','يتمنّاوا','يخذوا','وفاوا','يجاوا','ننحّيوا','يخلّيوا','نسربيوا','خلّاوا','حكاوا','تحكوا','يحكوا','تمشيوا','يهدوا','حشوا','ورّوا','يجروا','يبنيوا','ارتقيوا','يجيوا','وصّاوا','يجوا',]

# Clean/Normalize Arabic Text
def clean_str(text):
    #search = ["أ","إ","آ","ة","-","/",".","،"," و "," يا ",'"',"ـ","'","ى","\\",'\n', '\t','&quot;','?','؟','!']#,"_"
    #replace = ["ا","ا","ا","ه"," ","","",""," و"," يا","","","","ي","",' ', ' ',' ',' ? ',' ؟ ',' ! ']#," "
    search = ["أ","إ","آ","ة"," "]
    #"ة","-","/",".","،"," و "," يا ",'"',"ـ","'","ى","\\",'\n', '\t','&quot;','?','؟','!']#,"_"
    replace = ["ا","ا","ا","ه","_SPA_"]
    #"ه"," ","","",""," و"," يا","","","","ي","",' ', ' ',' ',' ? ',' ؟ ',' ! ']#," "

    #remove tashkeel
    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(p_tashkeel,"", text)
    
    #remove longation
    p_longation = re.compile(r'(.)\1+')
    subst = r"\1\1"
    text = re.sub(p_longation, subst, text)
    
    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = text.replace('اا', 'ا')
    
    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])
    
    #trim    
    text = text.strip()

    return text

def get_vec(n_model,dim, token):
    vec = np.zeros(dim)
    is_vec = False
    if token not in n_model.wv:
        _count = 0
        is_vec = True
        for w in token.split("_"):
            if w in n_model.wv:
                _count += 1
                vec += n_model.wv[w]
        if _count > 0:
            vec = vec / _count
    else:
        vec = n_model.wv[token]
    return vec

def calc_vec(pos_tokens, neg_tokens, n_model, dim):
    vec = np.zeros(dim)
    for p in pos_tokens:
        vec += get_vec(n_model,dim,p)
    for n in neg_tokens:
        vec -= get_vec(n_model,dim,n)
    
    return vec   

## -- Retrieve all ngrams for a text in between a specific range
def get_all_ngrams(text, nrange=3):
    text = re.sub(r'[\,\.\;\(\)\[\]\_\+\#\@\!\?\؟\^]', ' ', text)
    tokens = [token for token in text.split(" ") if token.strip() != ""]
    ngs = []
    for n in range(2,nrange+1):
        ngs += [ng for ng in ngrams(tokens, n)]
    return ["_".join(ng) for ng in ngs if len(ng)>0 ]

## -- Retrieve all ngrams for a text in a specific n
def get_ngrams(text, n=2):
    text = re.sub(r'[\,\.\;\(\)\[\]\_\+\#\@\!\?\؟\^]', ' ', text)
    tokens = [token for token in text.split(" ") if token.strip() != ""]
    ngs = [ng for ng in ngrams(tokens, n)]
    return ["_".join(ng) for ng in ngs if len(ng)>0 ]

## -- filter the existed tokens in a specific model
def get_existed_tokens(tokens, n_model):
    return [tok for tok in tokens if tok in n_model.wv ]
    
