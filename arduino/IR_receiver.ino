#include <IRremote.h>

int RECV_PIN = 4; // пин подключения ИК

IRrecv irrecv(RECV_PIN); // указываем вывод, к которому подключен приемник

decode_results results;

void setup()
{
  Serial.begin(9600); // выставляем скорость COM порта
  irrecv.enableIRIn(); // запускаем прием
}

void loop() {
  if (irrecv.decode(&results)) { // если данные пришли
    Serial.println(results.value); // печатаем данные
    irrecv.resume(); // принимаем следующую команду
  }
  delay(1000);
}
