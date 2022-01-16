class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: int,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        distance = round(self.distance, 3)
        ccal = round(self.calories, 3)
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {ccal}.')


class Training:
    """Базовый класс тренировки."""
    len_step = 0.65
    m_in_km = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.len_step / self.m_in_km
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.training_type,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    training_type = 'Бег'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coeff_calories_1 = 18
        coeff_calories_2 = 20
        time_in_min = self.duration * 60
        spent_calories = ((coeff_calories_1 * self.get_mean_speed()
                          - coeff_calories_2)
                          * self.weight / self.m_in_km
                          * time_in_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type = 'Спортивная ходьба'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 hight: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.hight = hight

    def get_spent_calories(self) -> float:
        coeff_calories_1 = 0.035
        coeff_calories_2 = 2
        coeff_calories_3 = 0.029
        time_in_min = self.duration * 60
        spent_calories = (
            (coeff_calories_1 * self.weight
             + (self.get_mean_speed() ** coeff_calories_2 // self.hight)
             * coeff_calories_3 * self.weight) * time_in_min
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    training_type = 'Плавание'
    len_step = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (self.length_pool
                      * self.count_pool / self.m_in_km
                      / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        coeff_calories_1 = 1.1
        coeff_calories_2 = 2
        spent_calories = ((self.get_mean_speed() + coeff_calories_1)
                          * coeff_calories_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        action = data[0]
        duration = data[1]
        weight = data[2]
        lenght_pool = data[3]
        count_pool = data[4]
        return Swimming(action,
                        duration,
                        weight,
                        lenght_pool,
                        count_pool)

    if workout_type == 'RUN':
        action = data[0]
        duration = data[1]
        weight = data[2]
        return Running(action,
                       duration,
                       weight)

    if workout_type == 'WLK':
        action = data[0]
        duration = data[1]
        weight = data[2]
        hight = data[3]
        return SportsWalking(action,
                             duration,
                             weight,
                             hight)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
