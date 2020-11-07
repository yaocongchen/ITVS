String str;
const byte SEG_PIN[6]={2, 3, 4, 5 ,6, 7};            // 7段顯示器的控制接腳
const byte NUM_OF_SEG = sizeof(SEG_PIN); // 7段顯示器的數量
int number_left=0;
int number_right=0;
int session_left=0;
int session_right=0;
byte digits[6] = {0, 0, 0, 0, 0, 0};

int button[2] = {0, 0};
int lang_btn=0;
int btn_start=0;
int btn_num=0;
const byte dataPin = 10;    // 74HC595序列輸入
const byte latchPin = 9;   // 74HC595暫存器時脈
const byte clockPin = 8;   // 74HC595序列時脈

//unsigned long previousMillis = 0;
//const long interval = 1000; 

const byte LEDs[10] = {             // 記錄0~9的七段數字
  0x7E, 0x30, 0x6D, 0x79, 0x33,//1111110   0110000
  0x5B, 0x5F, 0x70, 0x7F, 0x73
};
/*
void start_button(){
  if(digitalRead(13)== HIGH){
      button[0] =1;
  }else if (digitalRead(13)== LOW){
      button[0] =0;
  }
}
*/

//boolean  buttonUp = true;
void button_Features() {
  

  if(digitalRead(11)== HIGH){
      button[1] =1;
      //buttonUp =false;
  }
  //delay(10); // Delay 時間可視情況調整

  else if(digitalRead(12)== HIGH){
      button[1] =2;
      //buttonUp =false;
  }
  else if(digitalRead(11) != HIGH && digitalRead(12) != HIGH){
      button[1] =0;
      //buttonUp = true;
  }
  //delay(10); // Delay 時間可視情況調整
}

// 每隔一秒數字加1並拆解數字
void counter() {  
  /*unsigned long currentMillis = millis();
  // 每隔1秒執行一次底下的條件式內容
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
*/
  if (Serial.available()) {
    // 讀取傳入的字串直到"\n"結尾
    str = Serial.readStringUntil('\n');
    
      if (str == "num_left"){  
          number_left++;          
          Serial.println(number_left); // 回應訊息給電腦
      }else if(str == "num_right"){
          number_right++;
          Serial.println(number_right); // 回應訊息給電腦
      }

      if (number_left ==11 && number_right <10){
          session_left++;
          number_left=0;
          number_right=0;
      }else if(number_right ==11 && number_left <10){
          session_right++;
          number_left=0;
          number_right=0;
      }else if (number_left > 10 && number_left - number_right == 2){
          session_left++;
          number_left=0;
          number_right=0;
      }else if(number_right > 10 && number_right - number_left == 2){
          session_right++;
          number_left=0;
          number_right=0;
      }
    digits[0]= number_left % 10 ;       // 儲存個位數字(up)
    digits[1]= number_left / 10 % 10 ;  // 十位數字(up)
    digits[2]= number_right % 10 ;       // 儲存個位數字(down)
    digits[3]= number_right / 10 % 10 ;  // 十位數字(down)
    digits[4]= session_left;            // 顯示up勝場
    digits[5]= session_right;             // 顯示down勝場
    }
}

void display(){
  byte num;

  // 逐一設定每個七段顯示器
  for (byte i=0; i<NUM_OF_SEG; i++){
    num = digits[i];

    digitalWrite(latchPin, LOW);        // 關上閘門
    // 推入「LED」
    shiftOut(dataPin, clockPin, LSBFIRST, LEDs[num]);     // 推入「LED」
    digitalWrite(latchPin, HIGH);       // 開啟閘門
    
    digitalWrite(SEG_PIN[i], LOW);     // 點亮此顯示器
    delay(5);
    
    for (byte j=0; j<NUM_OF_SEG; j++) {
      digitalWrite(SEG_PIN[j], HIGH);  // 關閉所有顯示器
    }
  }
}

void setup() {
  Serial.begin(9600);

  pinMode(11, INPUT);
  pinMode(12, INPUT);
  
  pinMode(13, INPUT);
  /*
  pinMode(8, INPUT);

  */
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  
  for (byte i=0; i<NUM_OF_SEG; i++) {
    pinMode(SEG_PIN[i], OUTPUT);
    digitalWrite(SEG_PIN[i], HIGH);
  }
}
  
void loop() {
  
//start_button();
 button_Features();
 /*for(btn_num=0;btn_num<1;btn_num++)
    {
      Serial.print(button[btn_num]);
      delay(250);
      //break;
    }
    Serial.println("");  //換列
    */
 //boolean start = false;
 //if (start ==false){
 if ( btn_start != button[0]){
   //Serial.print(button[0]);
 }
 
   
   if (btn_num != button[1])
   {
      Serial.print(button[0]);
      Serial.print(button[1]);
      Serial.println("");
      
   }
 
   //Serial.println("");
   btn_start=button[0];
   btn_num = button[1];
  // start = true;
 //}
//Serial.print(button[0]);

  counter();
  display();
}
