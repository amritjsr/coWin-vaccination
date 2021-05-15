from time import sleep
import os
import sys
import requests
import datetime
from bs4 import BeautifulSoup
import re
# from playsound import playsound
import argparse

##### Variable Declaration 
state_list = []
district_list = []
state_district_mapping = []
numdays = 7
regex = re.compile(r'403 ERROR')
stateUrl = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
districtUrl = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}'
urlForSlotAvailability  = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"
return_error = {'return_code' : 'error'}


#### CREATING COLOR PALATE
class bcolors:
    HEADER = '\033[95m'
    OKSKYBLUE = '\x1b[1;36;40m'
    OKCYAN = '\033[96m'
    OKGREEN = '\x1b[1;32;40m'
    WARNING = '\033[93m'
    WARNINGBG = '\x1b[1;33;41m'
    MAGENTA = '\x1b[1;35;40m'
    OKRED = '\x1b[1;31;40m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#### THIS IS CLASS FOR SAVING THE CENTER INFO AS OBJECT
class center_info:
    def __init__(self, json_data):
        self.center_id = json_data['center_id']
        self.name = json_data['name']
        self.address = json_data['address']
        self.state_name = json_data['state_name']
        self.district_name = json_data['district_name']
        self.pincode = json_data['pincode']
        self.fee_type = json_data['fee_type']
        self.sessions = json_data['sessions']
    def print_center_available_45(self):
        # print(self.center_id, self.name, self.address,self.state_name)
        for session in self.sessions:
            if session['min_age_limit'] == 45 and session['available_capacity'] > 0 :
                textMsg = create_message(self.pincode, " => ", self.state_name, ' => ', self.name, " => ", self.district_name, " => " ,session['date'], " => ", session['available_capacity'], " => ", session['min_age_limit'], " => ", session['vaccine'], " => ", session['slots'], " =>  ", self.fee_type)
                if session['available_capacity'] < 10:
                    print(bcolors.WARNINGBG, textMsg , bcolors.ENDC)
                else:
                    print(bcolors.OKSKYBLUE, textMsg, bcolors.ENDC)

    def print_center_available_18(self):
        # print(self.center_id, self.name, self.address,self.state_name)
        for session in self.sessions:
            if session['min_age_limit'] == 18 and session['available_capacity'] > 0 :
                textMsg = create_message(self.pincode, " => ", self.state_name, ' => ', self.name, " => ", self.district_name, " => " ,session['date'], " => ", session['available_capacity'], " => ", session['min_age_limit'], " => ", session['vaccine'], " => ", session['slots'], " =>  ", self.fee_type)
                # response = send_msg_telegram_bot(textMsg)
                if session['available_capacity'] < 10:
                    print(bcolors.WARNINGBG, textMsg , bcolors.ENDC)
                else:
                    print(bcolors.OKSKYBLUE, textMsg, bcolors.ENDC)

    
    def print_center_info_available(self):
        # print(self.center_id, self.name, self.address,self.state_name)
        for session in self.sessions:
            if session['available_capacity'] > 0 :
                # os.system('say "Found"')
                textMsg = create_message(self.pincode, " => ", self.state_name, ' => ', self.name, " => ", self.district_name, " => " ,session['date'], " => ", session['available_capacity'], " => ", session['min_age_limit'], " => ", session['vaccine'], " => ", session['slots'], " =>  ", self.fee_type)
                # response = send_msg_telegram_bot(textMsg)
                if session['available_capacity'] < 10:
                    print(bcolors.WARNINGBG, textMsg, bcolors.ENDC)
                else:
                    if session['min_age_limit'] == 18:
                        print(bcolors.OKSKYBLUE, textMsg, bcolors.ENDC)
                    else:
                        print(bcolors.OKGREEN, textMsg, bcolors.ENDC)


headers = {
    'authority': 'cdn-api.co-vin.in',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7,bn;q=0.6,gu;q=0.5',
}

##### Function Declaration
def waiting(seconds = 0):
    for I in range(seconds, 0, -1):
        print("Waiting To Unblock -> ",I)
        sleep(1) 

def print_user_help():
    INTRO_STR = '''
            HELLO EVERYONE.... GOOD MORNING .....
            THIS PROGRAM IS MADE, SOLELY TO HELP PEOPLE FIND AVAILABLITY OF COVID VACCINE TO THEIR STATE AND NEARBY
            IF YOU ARE RUNNING THIS PROGRAM THE PLEASE DO THE FOLLOWING AS PRE-REQ
            1. INSTALL PYTHON3+
            2. python /path/to/script.py -s <state_codes with comas> -d <district_codes with comas> -a <0/18/45> [-l]

            THERE ARE FEW GUIDELINES TO RUN THIS CODE
            TOO MANY NUMBER OF REQUESTS CAN LEAD TO BLOCK THE IP-ADDRESS FOR NEXT 5MINS (That's why this script show waiting to unblock.....) 
            AND PLEASE DON'T RUN THIS SCRIPT TOO OFTEN WHICH OVERWELM THE API SERVER 

            THANKS,
            AMRITENDU DAS

            Please find the list of States and Their corrosponding District with their codes
        '''
    sleep(5)
    print(INTRO_STR)
    for id in state_list:
        print(id)
        print('-------------------------------------------------------------')
        print_districtList(id['state_id'])
        print('\n\n')
    print('\tRun Prog As => python /path/to/script.py -s <state_codes with comas> -d <district_codes with comas> -a <0/18/45> [-l]')
    print('\tBye Bye .....')
    return

def print_intro():
    INTRO_STR = '''
            HELLO EVERYONE.... GOOD MORNING .....\n
            THIS PROGRAM MADE, SOLELY TO HELP PEOPLE FIND AVAILABLITY OF COVID VACCINE TO THEIR STATE AND NEARBY\n
            IF YOU ARE RUNNING THIS PROGRAM THE PLEASE DO THE FOLLOWING AS PRE-REQ\n
            1. INSTALL PYTHON3+\n
            2. python /path/to/script.py -s <state_codes with comas> -d <district_codes with comas> -a <0/18/45>\n
            \n
            THERE ARE FEW GUIDELINES TO RUN THIS CODE\n
            TOO MANY NUMBER OF REQUESTS CAN LEAD TO BLOCK THE IP-ADDRESS FOR NEXT 5MINS (That's why this script show waiting to unblock.....) \n
            AND PLEASE DON'T RUN THIS SCRIPT TOO OFTEN WHICH OVERWELM THE API SERVER \n
            \n
            THANKS,\n
            AMRITENDU DAS\n
            \n
            Please find the list of States and Their corrosponding District with their codes with -l/--listAll options\n
        '''
    return INTRO_STR


def create_message(*args, **kwargs):
    text_msg = ''
    for item in args:
        text_msg = text_msg + str(item)
    return text_msg

def get_state_list():
    json_resp = requests.get(stateUrl, headers=headers)
    if json_resp.ok:
        return json_resp.json()['states']
    else:
        return return_error

def print_state_list():
    for state in state_list:
        print("[",state['state_name'], " <=> ", state['state_id'],"]")
            

def get_district_list(state_list = []):
    tempStateDistrictMap = []
    for state in state_list:
        json_resp = requests.get(districtUrl.format(state['state_id']), headers=headers)
        if json_resp.ok:
            tempMap = {state['state_id'] : json_resp.json()['districts']}
            tempStateDistrictMap.append(tempMap)
        else:
            return return_error

    return tempStateDistrictMap

def print_districtList(state_id):
    for state in state_district_mapping:
        if state_id in list(state.keys()):
            districts = (state.values())
            ctr = 1
            for district in list(*districts):
                if 4 / ctr == 1: 
                    ctr = 1;
                    print("[",district['district_name'], " <=> ", district['district_id'],"]     ")
                else:
                    ctr = ctr + 1
                    print("[",district['district_name'], " <=> ", district['district_id'],"]     ", end='')
            break
    return

def state_to_district_list(stateCode = 15):
    districtList = []
    for state in state_district_mapping:
        if stateCode in [*state.keys()]:
            for val in list(*state.values()):
                districtList.append(val['district_id'])
            return districtList


def get_user_input_env_var():
    envStateCodes = os.environ.get('STATE_CODE')
    envDistrictCode = os.environ.get('DISTRICT_CODE')

    if envStateCodes:
        stateCodes = list(map(lambda num: int(num), str(envStateCodes).strip().split(',')))
    else:
        return return_error
    
    if envDistrictCode:
        districtCodes = list(map(lambda num: int(num), str(envDistrictCode).strip().split(',')))
    else:
        return return_error  
    return stateCodes, districtCodes

def get_user_input_cmd_list():
    stateCodes = []
    districtCodes = []
    if len(sys.argv) ==  5:
        if ( '--state-code' == sys.argv[1] or '-s' == sys.argv[1]):
            stateCodes = stateCodes = list(map(lambda num: int(num), str(sys.argv[2]).strip().split(','))) 
        else:
            return return_error

        if ( '--dusrtict-code' == sys.argv[3] or '-d' == sys.argv[3]):
            districtCodes = list(map(lambda num: int(num), str(sys.argv[4]).strip().split(',')))
        else:
            return return_error
    else:
        return return_error

    return stateCodes, districtCodes


def districtCode_to_name(districtCode = 730):
    for state in state_district_mapping:
        for val in list(*state.values()):
            if districtCode == val['district_id']:
                return val['district_name']

def display_available_slots(stateCodes, districtCodes, age):
    base = datetime.datetime.today()
    date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
    date_str = [x.strftime("%d-%m-%Y") for x in date_list]
    urlError = []
    if str(districtCodes[0]) == '0':
        for state in stateCodes:
            dList = state_to_district_list(state)
            districtCodes.extend(dList)
    print('Displaing the slots available for next 7Days .... Starting from Today .... of Below Districts ....')
    for districtCode in districtCodes:  
        print('[ ', districtCode_to_name(districtCode), ' ]')
    for toDay in date_str:
        print('\n\nFOR DATE => ' + toDay)
        print('------------------------------')
        print('PINCODE   =>   STATE_NAME    =>    NAME    =>    DISTRICT_NAME     =>    SESSION[\'DATE\']    =>      AVAILABLE_CAPACITY    =>     MIN_AGE_LIMIT     =>     VACCINE-NAME    =>     SLOTS     =>     FEE_TYPE ')
        for district in districtCodes:
            # print(URL_FOR_AVAILABILITY)
            # print(" Searching For =>  ",district, "  => ", URL_FOR_AVAILABILITY)
            url = urlForSlotAvailability.format(district, toDay)
            ctr = 5
            for I in range(6):
                json_resp = requests.get(url,headers=headers)
                if json_resp.ok:
                    break
                else:
                    bsh = BeautifulSoup(json_resp.text, 'html.parser')
                    # print(bsh.h1)
                    if regex.search(str(bsh.h1)):
                        print('403 Error : Fobiden, Waiting for 65 Sec .... ')
                        waiting(65)
                        print('Retrying => ', url)
                        
            if json_resp.ok:
                json_data = json_resp.json()
                # sys.exit()
                for center in json_data['centers']:
                    temp_cls_cntr_info = center_info(center)
                    if age == 18:
                        temp_cls_cntr_info.print_center_available_18()
                    elif age == 45:
                        temp_cls_cntr_info.print_center_available_18()
                    elif age == 0:
                        temp_cls_cntr_info.print_center_info_available()
                    else:
                        print()
            else:
                print("Can't Fetch => ", url, "  Giving Up!!!!!!")
                urlError.append(url)
                print(json_resp.text)
                    # print(type(center))
                # sys.exit()
        # sys.exit()
        if len(urlError) > 0:
            print('Below URL can\'t be reach right now, retry again ..... ')
            print(urlError)
    pass

def send_msg_telegram_bot(bot_message):
    p = re.compile('=')
    #How to configure chatBot with botFather TeleGram => https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot
    telegram_reserv_char = "_*[]()~`>#+-=|{}.!"    #YOU MESSAGE SHOULDN'T HAVE THESE CHARECTORS
    bot_token_id = 'ABCD1234XYZ'
    bot_chat_id = '123123423423'
    txt = ''.join(['\\' + c if c in telegram_reserv_char else c for c in bot_message]) #PLACING \ BEFORE RESERVE CHAR
    send_message = 'https://api.telegram.org/bot' + bot_token_id + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=MarkdownV2&text=' + txt
    response = requests.get(send_message)

    return response.json()   



if __name__ == '__main__':
    
    state_list = get_state_list()
    state_district_mapping = get_district_list(state_list=state_list)
    parser=argparse.ArgumentParser(description=print_intro())
    parser.add_argument("-s","--stateCode", help="State Code in Numeric, comma separated if more that one")
    parser.add_argument("-d","--districtCode", default='0' ,help="District Code in Numeric, comma separated if more that one")
    parser.add_argument("-a","--age", type=int, default=0, help="Age in Numeric, 18 or 45 or 0(For All Ages)")
    parser.add_argument('-l','--listAll', action='store_true', help = 'Listing All State Codes and Disctrict Codes' )
    args = parser.parse_args()
    # print(args.__dict__)
    # sys.exit()
    
    # returnCodeCmd = get_user_input_cmd_list()
    # # print(type(returnCodeCmd), returnCodeCmd)
    # if returnCodeCmd == return_error:
    #     returnCodeEnv = get_user_input_env_var()
    #     if returnCodeEnv == return_error:
    #         print_user_help()
    #     else:
    #         stateCodes, districtCodes = returnCodeEnv
    # else:
    #     stateCodes, districtCodes = returnCodeCmd
    
    cmdStateCodes = args.stateCode
    cmdDistrictCodes = args.districtCode
    age = args.age
    listAll = args.listAll
    print(cmdStateCodes, cmdDistrictCodes, age, listAll)

    if cmdStateCodes:
        stateCodes = list(map(lambda num: int(num), cmdStateCodes.strip().split(',')))
    else:
        print_user_help()
        sys.exit(0)

    if cmdDistrictCodes:
        districtCodes = list(map(lambda num: int(num), cmdDistrictCodes.strip().split(',')))
    else:
        print_user_help()
        
    # print(stateCodes, districtCodes, age, listAll)
    # print(state_district_mapping)
    # print(state_to_district_list(36))
    # sys.exit()
    if listAll == True:
        print_user_help()
        sys.exit(0)
    else:
        display_available_slots(stateCodes, districtCodes, age)
    
