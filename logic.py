from random import randint
import requests
from datetime import datetime, timedelta


class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.color = self.get_color()
        self.hp = randint(200,400)
        self.power = randint(30,60)
        self.last_feed_time = datetime.now()
        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data["sprites"]["other"]["official-artwork"]["front_default"])
        else:
            return "https://upload.wikimedia.org/wikipedia/ru/7/77/Pikachu.png"        
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    def get_color(self):
        url = f'https://pokeapi.co/api/v2/pokemon-species/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data["color"]["name"])
        else:
            return "yellow" 
                
    # Метод класса для получения информации
    def info(self):
        return f"""Имя твоего покемона: {self.name}
                Цвет твоего покемона: {self.color}
                Сила твоего покемона: {self.power}
                Здоровье твоего покемона: {self.hp}"""


    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
    
    # Метод атаки
    def attack(self, enemy):
        if isinstance(enemy, Wizard):
            oryshie = randint(1,5)
            if oryshie == 1:
                return("Волшебник заблокировал атаку")
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "        


    def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time + delta_time}"


class Wizard(Pokemon):
    def info(self):
        return("Вы волшебник" + super().info())

    def feed(self):
        return super().feed(feed_interval=15)


class Fighter(Pokemon):
    def info(self):
        return("Вы боец" + super().info())
    
    def feed(self):
        return super().feed(hp_increase=15)

    def attack(self, enemy):
        super_power = randint(5,15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -=  super_power
        return result + f"Боец получил прибафку к урону: {super_power}"
