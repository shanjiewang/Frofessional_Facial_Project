from flask import Flask, request,render_template, url_for
from flask_moment import Moment
from datetime import datetime
from pathlib import Path
import uuid
import recognition.flask as model

app = Flask(__name__)
moment = Moment(app)

# practice 回上一層去找 uploaded 這個資料夾
UPLOAD_FOLDER = Path(__file__).resolve().parent/'static/uploaded'
# ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif','heic'])
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 3000 * 3000 # 16MB 設定上傳最大檔案接受多大

@app.route('/')
def index():
    return render_template("types_index.html",src = url_for('static', filename=f'css/stylesF.css'))

#----------practice start------------
@app.route('/')
def test_static():
    print(app.url_map)
    return render_template('types_index.html')
#----------practice end-------------- 

@app.route('/aboutMe')
def aboutMe():
    return render_template("aboutWeF.html",src = url_for('static', filename=f''))

@app.route('/mailMe')
def mailMe():
    return render_template("mailMeF.html",src = url_for('static', filename=f''))

@app.route('/uploadPhoto')
def muploadPhoto():
    return render_template("uploadPhotoF.html",src = url_for('static', filename=f''))

@app.route('/resultPhoto', methods=['GET', 'POST'])
def resultPhoto():
    
    if request.method == "GET":
        noface='noface'
        return render_template('uploadPhotoF.html', noface=noface)
        # return render_template('uploadPhotoF.html', page_header="upload file")
    elif request.method == "POST":
        noface='haveface'
        file = request.files['file'] # 讀取 post uploadphoto.html 帶著照片進來的  # request.files['file'] 相對應 name="file" 名字要一樣才取得到
        # user = User(request.form.get("name"), request.form.get("email"), request.form.get("password")
        yourName =request.form['yourName']
        yourLikeTypes =request.form['yourLikeTypes']
        if file:
            
            #filename = secure_filename(file.filename) # 直接用原檔名取新名
            filename = str(uuid.uuid4())+".jpg"  # uuid4 碼 = 新檔名  要去除中文檔名
            file.save(app.config['UPLOAD_FOLDER']/filename)
            # yourLikeTypes="ordinary_people"

            filenameSplit=[]
            filenameSplit=filename.split('.')

            predict = model.main(filename,yourLikeTypes)  # 把上傳的檔案傳給模型 預測結果數字會自己出來 讀取模型結果 你是{{ predict }}型  

            if predict!="Noface":

                predictTypes=predict[0]   

                if predictTypes=="boss":       
                    fi1=filenameSplit[0]+'_'+predictTypes+'_Nosehead_W.jpg'
                    fi2=filenameSplit[0]+'_'+predictTypes+'_Lip_width_W.jpg'
                    fi3=filenameSplit[0]+'_'+predictTypes+'_Eye_R_B_W.jpg'  
                    fi4=filenameSplit[0]+'_'+predictTypes+'_Eyebrow_dis_W.jpg'
                    fi5=filenameSplit[0]+'_'+predictTypes+'_philtrum_length_L.jpg'
                    fi6=filenameSplit[0]+'_'+yourLikeTypes+'_Nosehead_W.jpg'
                    fi7=filenameSplit[0]+'_'+yourLikeTypes+'_Lip_width_W.jpg'
                    fi8=filenameSplit[0]+'_'+yourLikeTypes+'_Eye_R_B_W.jpg'
                    fi9=filenameSplit[0]+'_'+yourLikeTypes+'_Eyebrow_dis_W.jpg'
                    fi10=filenameSplit[0]+'_'+yourLikeTypes+'_philtrum_length_L.jpg'
                    fi0=filenameSplit[0]+'_res.jpg' 
                    predictTypes="你相當大的機會有成為「企業家」的潛力，下一個郭台銘就是你!!"
                    predictName="「企業家」"

                elif predictTypes=="ordinary_people":                
                    fi1=filenameSplit[0]+'_'+predictTypes+'_Nosehead_W.jpg'
                    fi2=filenameSplit[0]+'_'+predictTypes+'_Lip_width_W.jpg'
                    fi3=filenameSplit[0]+'_'+predictTypes+'_Eye_R_B_W.jpg'  
                    fi4=filenameSplit[0]+'_'+predictTypes+'_Eyebrow_dis_W.jpg'
                    fi5=filenameSplit[0]+'_'+predictTypes+'_philtrum_length_L.jpg'
                    fi6=filenameSplit[0]+'_'+yourLikeTypes+'_Nosehead_W.jpg'
                    fi7=filenameSplit[0]+'_'+yourLikeTypes+'_Lip_width_W.jpg'
                    fi8=filenameSplit[0]+'_'+yourLikeTypes+'_Eye_R_B_W.jpg'
                    fi9=filenameSplit[0]+'_'+yourLikeTypes+'_Eyebrow_dis_W.jpg'
                    fi10=filenameSplit[0]+'_'+yourLikeTypes+'_philtrum_length_L.jpg'
                    fi0=filenameSplit[0]+'_res.jpg' 
                    predictTypes="你沒有被辨認出最可能成為哪種職業，代表你有無限的可能，「平凡人」也能有不平凡的成就!!"
                    predictName="「平凡人」"

                elif predictTypes=="entertainer":               
                    fi1=filenameSplit[0]+'_'+predictTypes+'_Nosehead_W.jpg'
                    fi2=filenameSplit[0]+'_'+predictTypes+'_Lip_width_W.jpg'
                    fi3=filenameSplit[0]+'_'+predictTypes+'_Eye_R_B_W.jpg'  
                    fi4=filenameSplit[0]+'_'+predictTypes+'_Eyebrow_dis_W.jpg'
                    fi5=filenameSplit[0]+'_'+predictTypes+'_philtrum_length_L.jpg'
                    fi6=filenameSplit[0]+'_'+yourLikeTypes+'_Nosehead_W.jpg'
                    fi7=filenameSplit[0]+'_'+yourLikeTypes+'_Lip_width_W.jpg'
                    fi8=filenameSplit[0]+'_'+yourLikeTypes+'_Eye_R_B_W.jpg'
                    fi9=filenameSplit[0]+'_'+yourLikeTypes+'_Eyebrow_dis_W.jpg'
                    fi10=filenameSplit[0]+'_'+yourLikeTypes+'_philtrum_length_L.jpg'
                    fi0=filenameSplit[0]+'_res.jpg' 
                    predictTypes="你有很高的機率成為「藝人」，出門要小心，免得星探找上你!!"  
                    predictName="「藝人」"

                elif predictTypes=="doctor":
                    fi1=filenameSplit[0]+'_'+predictTypes+'_Nosehead_W.jpg'
                    fi2=filenameSplit[0]+'_'+predictTypes+'_Lip_width_W.jpg'
                    fi3=filenameSplit[0]+'_'+predictTypes+'_Eye_R_B_W.jpg'  
                    fi4=filenameSplit[0]+'_'+predictTypes+'_Eyebrow_dis_W.jpg'
                    fi5=filenameSplit[0]+'_'+predictTypes+'_philtrum_length_L.jpg'
                    fi6=filenameSplit[0]+'_'+yourLikeTypes+'_Nosehead_W.jpg'
                    fi7=filenameSplit[0]+'_'+yourLikeTypes+'_Lip_width_W.jpg'
                    fi8=filenameSplit[0]+'_'+yourLikeTypes+'_Eye_R_B_W.jpg'
                    fi9=filenameSplit[0]+'_'+yourLikeTypes+'_Eyebrow_dis_W.jpg'
                    fi10=filenameSplit[0]+'_'+yourLikeTypes+'_philtrum_length_L.jpg'
                    fi0=filenameSplit[0]+'_res.jpg' 
                    predictTypes="我希望未來健康檢查時才會遇見你，因為你有很可能是個專業的「醫師」!!" 
                    predictName="「醫師」"

                elif predictTypes=="politician":
                    fi1=filenameSplit[0]+'_'+predictTypes+'_Nosehead_W.jpg'
                    fi2=filenameSplit[0]+'_'+predictTypes+'_Lip_width_W.jpg'
                    fi3=filenameSplit[0]+'_'+predictTypes+'_Eye_R_B_W.jpg'  
                    fi4=filenameSplit[0]+'_'+predictTypes+'_Eyebrow_dis_W.jpg'
                    fi5=filenameSplit[0]+'_'+predictTypes+'_philtrum_length_L.jpg'
                    fi6=filenameSplit[0]+'_'+yourLikeTypes+'_Nosehead_W.jpg'
                    fi7=filenameSplit[0]+'_'+yourLikeTypes+'_Lip_width_W.jpg'
                    fi8=filenameSplit[0]+'_'+yourLikeTypes+'_Eye_R_B_W.jpg'
                    fi9=filenameSplit[0]+'_'+yourLikeTypes+'_Eyebrow_dis_W.jpg'
                    fi10=filenameSplit[0]+'_'+yourLikeTypes+'_philtrum_length_L.jpg'
                    fi0=filenameSplit[0]+'_res.jpg' 
                    predictTypes="你有成為「政治家」的潛力，相信你就是政治界的那股清流!!" 
                    predictName="「政治家」"

                elif predictTypes=="sport":   
                    fi1=filenameSplit[0]+'_'+predictTypes+'_Nosehead_W.jpg'
                    fi2=filenameSplit[0]+'_'+predictTypes+'_Lip_width_W.jpg'
                    fi3=filenameSplit[0]+'_'+predictTypes+'_Eye_R_B_W.jpg'  
                    fi4=filenameSplit[0]+'_'+predictTypes+'_Eyebrow_dis_W.jpg'
                    fi5=filenameSplit[0]+'_'+predictTypes+'_philtrum_length_L.jpg'
                    fi6=filenameSplit[0]+'_'+yourLikeTypes+'_Nosehead_W.jpg'
                    fi7=filenameSplit[0]+'_'+yourLikeTypes+'_Lip_width_W.jpg'
                    fi8=filenameSplit[0]+'_'+yourLikeTypes+'_Eye_R_B_W.jpg'
                    fi9=filenameSplit[0]+'_'+yourLikeTypes+'_Eyebrow_dis_W.jpg'
                    fi10=filenameSplit[0]+'_'+yourLikeTypes+'_philtrum_length_L.jpg'
                    fi0=filenameSplit[0]+'_res.jpg' 
                    predictTypes="你非常有成為「運動員」的資質，期待在奧運上看到充滿運動細胞的你!!" 
                    predictName="「運動員」"
                else:
                    predictTypes="請上傳正常照片"

                #     yourLikeTypesListEng=['boss','ordinary_people','entertainer','doctor','politician','sport']
                #     yourLikeTypesListUtf=['「企業家」','「平凡人」','「藝人」','「醫師」','「政治家」','「運動員」']

                # for j in range(len(yourLikeTypesListEng)):
                #     if yourLikeTypesListEng[j]==yourLikeTypesListUtf[j]:
                #         yourLikeTypesListEng[j]=yourLikeTypesListUtf[j]

                if yourLikeTypes=='boss':
                    yourLikeTypes="「企業家」"
                elif yourLikeTypes=='ordinary_people':
                    yourLikeTypes="「平凡人」"
                elif yourLikeTypes=='entertainer':
                    yourLikeTypes="「藝人」"
                elif yourLikeTypes=='doctor':
                    yourLikeTypes="「醫師」"
                elif yourLikeTypes=='politician':
                    yourLikeTypes="「政治家」"
                elif yourLikeTypes=='sport':
                    yourLikeTypes="「運動員」"

                if yourLikeTypes==predictName:
                    sameTypes='YES'
                else: 
                    sameTypes='NO' 
        
                p=[0,1,2,3,4,5,6,7,8,9,10]

                # 照片相像星級  
                for i in range(11):
                    if predict[i]==5:
                        p[i]='✮✮✮✮✮'
                    elif predict[i]==4:
                        p[i]='✮✮✮✮'
                    elif predict[i]==3:
                        p[i]='✮✮✮'
                    elif predict[i]==2:
                        p[i]='✮✮'
                    elif predict[i]==1:
                        p[i]='✮'
                    else: 
                        p[i]='回傳失敗'
            
                        print(p[i])
                
                # if predict[1]==5:
                #     p1='✮✮✮✮✮'
                # elif predict[1]==3:
                #     p1='✮✮✮'
                # else: 
                #     p1='✮'
                
                data = [["method:",  sameTypes+'_'+predictName+'_'+yourLikeTypes],
                ["base_url:", request.base_url],
                ["file:",fi2],
                ["file123:",predict]]

                return render_template('resultPhotoF.html', page_header="review file", data=data, predictTypes = predictTypes, sameTypes=sameTypes,predictName=predictName,yourName = yourName,yourLikeTypes = yourLikeTypes,noface=noface, src = url_for('static', filename=f'uploaded/{fi0}'),
                a1 = url_for('static', filename=f'uploaded/{fi1}'),a2 = url_for('static', filename=f'uploaded/{fi2}'),a3 = url_for('static', filename=f'uploaded/{fi3}'),a4 = url_for('static', filename=f'uploaded/{fi4}'),a5 = url_for('static', filename=f'uploaded/{fi5}'),
                a6 = url_for('static', filename=f'uploaded/{fi6}'),a7 = url_for('static', filename=f'uploaded/{fi7}'),a8 = url_for('static', filename=f'uploaded/{fi8}'),a9 = url_for('static', filename=f'uploaded/{fi9}'),a10 = url_for('static', filename=f'uploaded/{fi10}'),
                p1= p[1],p2 = p[2],p3 = p[3],p4 = p[4],p5 = p[5],p6 = p[6],p7 = p[7],p8 = p[8],p9 = p[9],p10 = p[10])

            else: 
                noface='noface'
                return render_template('noFace.html')
                # return render_template('uploadPhotoF.html', noface=noface)


if __name__=="__main__":
    app.run(debug=True)