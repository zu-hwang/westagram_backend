import bcrypt , json, jwt

from config.util      import login_required
from django.shortcuts import render
from django.views     import View
from django.http      import JsonResponse

# DB가져오기
from .models import User
# 알고리즘, 비밀키 가져오기
from config.my_settings import SECRET_KEY, ALGORITHM


def check_password( db_pw, input_pw):
    byte_db_pw = db_pw.encode('utf-8') # 복화화를 위해 바이트로 변형 
    byte_input_pw = input_pw.encode('utf-8')   # 복화화를 위해 바이트로 변형
    result = bcrypt.checkpw(byte_input_pw, byte_db_pw) # 해쉬하여 값비교 > T/F 결과 리턴
    return result



class SignUp(View):
    def post(self, req):
        data      = json.loads(req.body)
        # print('username -', data['user_name'])
        # print('password -', data['password'])
        user_name = data['user_name']
        password  = data['password']

        # ? 비밀번호 암호화
        salt = bcrypt.gensalt() # bytes salt
        password = password.encode('utf-8') # 입력받은 비밀번호 bytes로 인코딩
        hashed_password = bcrypt.hashpw(password, salt) # 인자로 바이트비번, 바이트솔트 넣기
        str_hashed_password = hashed_password.decode('utf-8') # DB에 넣기 위해 문자열로 변환
        
        if User.objects.filter(user_name=user_name).exists():
            return JsonResponse({'message': '사용할수 없는 아이디'}, status=400)
        else:
            User(user_name=user_name, password=str_hashed_password).save()
            # ! save()보다 create 사용하는 것을 추천한다
            # 왜냐하면, create로 하면 테이블을 생성, 변수에 담아 쓸수 있다.
            # 왜 그래야 하느냐? 쿼리 효율을 생각해야 한다. 한번 DB에 접근하면 비용이 발생한다.
            # 만약 지금 저장한 데이터를 다시 불러서 로직을 짜야 한다면. get(), filter() 써야 하는데
            # create로 변수를 담으면 DB에 접근할 필요없어 비용을 아낄수 있고,
            # 귀찮음을 격지 않아도 된다(테이블 목록 가져와서 몇번 인덱스에 필드명 뭐시기 가져와라 같은..)
            return JsonResponse({'message': '성공'}, status=200)


class SignIn(View):
    # 비밀번호 체크
    try : 
        def post(self, req):
            data      = json.loads(req.body)
            # password  = data['password'] # ! 데이터는 날거로 받는것보다 get(_ , None)과 같이 에러를 잡아 줄 수 있게 가져오는 것이 좋다.
            user_name = data.get('user_name' , None)
            password = data.get('password' , None)
            user_info = User.objects.filter(user_name=user_name)
            # print('유저네임: ', user_info[0].user_name)
            if user_info:  # 유저정보가 있을 때
                if user_info[0].user_name == user_name and check_password(user_info[0].password, password):
                  # jwt로 encode하면 byte로 바뀐다 그래서 문자열로 변환하는 것이 필요하다. 변환은 decode('utf-8')을 통해 진행한다. .. 만약 디코드 안하고 응답보내면 500에러~~
                    token = jwt.encode({'user_name': user_name}, SECRET_KEY['secret'], ALGORITHM)
                    return JsonResponse({'token': token.decode('utf-8')}, status=200)
                else:
                    return JsonResponse({'message': '비밀번호 틀림'}, status=400)
            else:
                return JsonResponse({'message':'UNAUTHORIZED'}, status=401)
    except TypeError:
        JsonResponse({"message" : '타입에러다'}, status=400)


    # ? try & except 를 어떻게 언제 쓰야할까
    # ! status.. 음 어떻게 보내야 할까나 ? 
