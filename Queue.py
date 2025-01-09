from Logger import log_error, log_warning
import time

class Queue:
    def __init__(self, window_size=35):
        """
        De queue class houdt het aantal mensen, capiciteit en wachttijd bij.
        :param window_size: de grootte van het venster waarin de wachttijd wordt berekend
        """
        self.window_size = window_size
        self.people_in_queue = 0
        self.exited_people = []

    def add_person(self):
        """
        Voeg een persoon toe aan de wachtrij. (begin)
        """
        self.people_in_queue += 1

    def remove_person(self):
        """
        Verwijder een persoon uit de wachtrij. (einde)
        """
        if self.people_in_queue > 0:
            self.people_in_queue -= 1
            self.append_exit_time()
        else:
            log_warning("remove_person() terwijl wachtrij leeg is!")

    def append_exit_time(self):
        """
        Voeg sample toe aan de wachtrij exit venster.
        """
        self.exited_people.append(time.time())

        if len(self.exited_people) > self.window_size:
            self.exited_people.pop(0)

    def get_hourly_capacity(self):
        """
        Bereken capicititeit van de wachtrij in verlatende mensen per uur.
        """
        if len(self.exited_people) < 2:
            return 0

        first = self.exited_people[0]
        last = self.exited_people[-1]
        time_diff = last - first

        # aantal mensen dat de wachtrij kunnen verlaten in 1 uur
        # gaat ervan uit dat de window representatief is voor de wachtrij
        return int((len(self.exited_people) / time_diff) * 3600)

    def get_queue_length(self):
        """
        Lengte van wachtrij (aantal mensen)
        :return:
        """
        return self.people_in_queue

    def get_queue_duration_hours(self):
        """
        Wachttijd van de wachtrij in uren.
        """
        capacity = self.get_hourly_capacity()

        if capacity == 0:
            return 0

        return self.people_in_queue / capacity

    def get_queue_duration_minutes(self):
        """
        Wachttijd van de wachtrij in minuten.
        """
        return self.get_queue_duration_hours() * 60

    def get_queue_duration_aligned_minutes(self, alignment=5):
        """
        Geef de wachtrij in intervallen van alignment minuten.
        :param alignment: interval in minuten
        :return:
        """
        duration = self.get_queue_duration_minutes() + alignment # afronden naar boven
        return duration - (duration % alignment)


