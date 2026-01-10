import pygame
from settings import *

class TimeSystem:
    def __init__(self):
        self.time = 6.0  # Start at 6 AM
        self.day = 1
        self.season = "Spring"
        self.seasons = ["Spring", "Summer", "Fall", "Winter"]
        self.days_per_season = 10
        self.time_speed = TIME_SPEED
        
    def update(self, dt=1):
        """Update time"""
        self.time += self.time_speed * dt
        
        if self.time >= 24:
            self.time = 0
            self.day += 1
            
            # Change season
            if self.day % self.days_per_season == 0:
                season_index = (self.seasons.index(self.season) + 1) % len(self.seasons)
                self.season = self.seasons[season_index]
                
    def is_night(self):
        """Check if it's nighttime"""
        return self.time >= NIGHT_START or self.time < NIGHT_END
        
    def get_time_string(self):
        """Get formatted time string"""
        hour = int(self.time)
        minute = int((self.time - hour) * 60)
        
        # Convert to 12-hour format
        if hour == 0:
            hour_12 = 12
            period = "AM"
        elif hour < 12:
            hour_12 = hour
            period = "AM"
        elif hour == 12:
            hour_12 = 12
            period = "PM"
        else:
            hour_12 = hour - 12
            period = "PM"
            
        return f"{hour_12}:{minute:02d} {period}"
        
    def get_darkness_alpha(self):
        """Get darkness overlay alpha based on time"""
        if NIGHT_END <= self.time < NIGHT_START:
            # Daytime - no darkness
            if self.time < 8:
                # Dawn - gradually brighten
                return int(150 * (1 - (self.time - NIGHT_END) / 2))
            elif self.time > 16:
                # Dusk - gradually darken
                return int(150 * ((self.time - 16) / 2))
            return 0
        else:
            # Nighttime
            return 180
            
    def get_day_string(self):
        """Get day and season string"""
        return f"{self.season} {self.day % self.days_per_season + 1}"