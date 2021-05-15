    HELLO EVERYONE.... GOOD MORNING .....
    THIS PROGRAM IS MADE, SOLELY TO HELP PEOPLE FIND AVAILABLITY OF COVID VACCINE TO THEIR STATE AND NEARBY
    IF YOU ARE RUNNING THIS PROGRAM THE PLEASE DO THE FOLLOWING AS PRE-REQ
    1. INSTALL PYTHON3+
    3. pip install requests, bs4, argparse
    3. python /path/to/coWinSlotFinder.py -s <state_codes with comas> -d <district_codes with comas> -a <0/18/45> [-l]

    THERE ARE FEW GUIDELINES TO RUN THIS CODE
    TOO MANY NUMBER OF REQUESTS CAN LEAD TO BLOCK THE IP-ADDRESS FOR NEXT 5MINS (That's why this script show waiting to unblock.....) 
    AND PLEASE DON'T RUN THIS SCRIPT TOO OFTEN WHICH OVERWELM THE API SERVER 

    How to Run this Program.
    1. First time you please run python /path/to/coWinSlotFinder.py -h
        This will give you all State & it's corrosponding Districts list,Please note down your required state & district codes
    2. Second time run this program with  python /path/to/coWinSlotFinder.py -s <state_codes with comas> -d <district_codes with comas> -a <0/18/45>
    -a age  = 0 for all available slots
            = 18 for all 18-44 available slots
            = 45 for all 45+ available slots

    This program has capablity to send you notification to telegram, but for that you have to configure chatbot using telegram botFather and gather token-id and chat-id
    for that many youTube videos are available.
    
    THANKS,
            