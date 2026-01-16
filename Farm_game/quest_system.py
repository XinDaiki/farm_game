import pygame
from settings import *

class Quest:
    """Individual quest with objectives and rewards"""
    def __init__(self, quest_id, title, description, objectives, rewards, prerequisite=None):
        self.id = quest_id
        self.title = title
        self.description = description
        self.objectives = objectives  # List of (type, target, amount, current)
        self.rewards = rewards  # Dict: {"money": amount, "items": {item: count}}
        self.prerequisite = prerequisite  # Quest ID that must be completed first
        self.completed = False
        self.claimed = False
        
    def update_progress(self, obj_type, target, amount=1):
        """Update objective progress"""
        for i, obj in enumerate(self.objectives):
            if obj["type"] == obj_type and obj["target"] == target:
                self.objectives[i]["current"] = min(
                    obj["current"] + amount,
                    obj["amount"]
                )
                
    def is_complete(self):
        """Check if all objectives are complete"""
        for obj in self.objectives:
            if obj["current"] < obj["amount"]:
                return False
        return True
    
    def get_progress_text(self):
        """Get progress text for UI"""
        lines = []
        for obj in self.objectives:
            current = obj["current"]
            target = obj["amount"]
            desc = obj["description"]
            status = "✓" if current >= target else f"{current}/{target}"
            lines.append(f"{status} {desc}")
        return lines

class QuestSystem:
    """Manages all quests in the game"""
    def __init__(self):
        self.quests = {}
        self.active_quests = []
        self.completed_quests = []
        self.show_quest_tab = False
        self.selected_quest = None
        
        # Fonts
        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 16)
        
        # Initialize quests
        self.init_quests()
        
        # Auto-start first quest
        self.start_quest("welcome")
        
    def init_quests(self):
        """Initialize all available quests"""
        
        # Tutorial/Starter Quests
        self.quests["welcome"] = Quest(
            "welcome",
            "Welcome to the Farm!",
            "Learn the basics of farming in Harvest Valley.",
            [
                {"type": "till", "target": "soil", "amount": 3, "current": 0, 
                 "description": "Till 3 soil patches"},
                {"type": "plant", "target": "wheat", "amount": 2, "current": 0,
                 "description": "Plant 2 wheat seeds"},
            ],
            {"money": 50, "items": {"wheat_seed": 5}},
            prerequisite=None
        )
        
        self.quests["first_harvest"] = Quest(
            "first_harvest",
            "First Harvest",
            "Water and harvest your first crops.",
            [
                {"type": "water", "target": "crop", "amount": 3, "current": 0,
                 "description": "Water crops 3 times"},
                {"type": "harvest", "target": "wheat", "amount": 2, "current": 0,
                 "description": "Harvest 2 wheat"},
            ],
            {"money": 100, "items": {"carrot_seed": 3}},
            prerequisite="welcome"
        )
        
        self.quests["claim_land"] = Quest(
            "claim_land",
            "Expand Your Farm",
            "Claim plots to expand your farming operation.",
            [
                {"type": "claim", "target": "plot", "amount": 5, "current": 0,
                 "description": "Claim 5 plots"},
            ],
            {"money": 200, "items": {"wood": 10}},
            prerequisite="first_harvest"
        )
        
        # Farming Quests
        self.quests["diverse_farm"] = Quest(
            "diverse_farm",
            "Diversify Your Crops",
            "Plant different types of crops.",
            [
                {"type": "plant", "target": "carrot", "amount": 3, "current": 0,
                 "description": "Plant 3 carrots"},
                {"type": "plant", "target": "tomato", "amount": 2, "current": 0,
                 "description": "Plant 2 tomatoes"},
            ],
            {"money": 150, "items": {"corn_seed": 2, "tomato_seed": 3}},
            prerequisite="first_harvest"
        )
        
        self.quests["master_farmer"] = Quest(
            "master_farmer",
            "Master Farmer",
            "Harvest a variety of crops to become a master farmer.",
            [
                {"type": "harvest", "target": "wheat", "amount": 10, "current": 0,
                 "description": "Harvest 10 wheat"},
                {"type": "harvest", "target": "carrot", "amount": 5, "current": 0,
                 "description": "Harvest 5 carrots"},
                {"type": "harvest", "target": "tomato", "amount": 5, "current": 0,
                 "description": "Harvest 5 tomatoes"},
            ],
            {"money": 500, "items": {"corn_seed": 5}},
            prerequisite="diverse_farm"
        )
        
        # Resource Quests
        self.quests["lumberjack"] = Quest(
            "lumberjack",
            "Lumberjack",
            "Gather wood for crafting.",
            [
                {"type": "collect", "target": "wood", "amount": 20, "current": 0,
                 "description": "Collect 20 wood"},
            ],
            {"money": 100, "items": {}},
            prerequisite=None
        )
        
        self.quests["crafting_basics"] = Quest(
            "crafting_basics",
            "Learn to Craft",
            "Craft items to improve your farm.",
            [
                {"type": "craft", "target": "fence", "amount": 2, "current": 0,
                 "description": "Craft 2 fences"},
            ],
            {"money": 150, "items": {"wood": 15}},
            prerequisite="lumberjack"
        )
        
        # Animal Quests
        self.quests["animal_friend"] = Quest(
            "animal_friend",
            "Friend of Animals",
            "Take care of your animals.",
            [
                {"type": "feed", "target": "animal", "amount": 5, "current": 0,
                 "description": "Feed animals 5 times"},
                {"type": "collect", "target": "egg", "amount": 3, "current": 0,
                 "description": "Collect 3 eggs"},
            ],
            {"money": 200, "items": {}},
            prerequisite="first_harvest"
        )
        
        # Money Quests
        self.quests["entrepreneur"] = Quest(
            "entrepreneur",
            "Entrepreneur",
            "Build up your savings.",
            [
                {"type": "money", "target": "total", "amount": 500, "current": 0,
                 "description": "Earn $500 total"},
            ],
            {"money": 250, "items": {"corn_seed": 3}},
            prerequisite="first_harvest"
        )
        
        self.quests["rich_farmer"] = Quest(
            "rich_farmer",
            "Rich Farmer",
            "Become wealthy through farming.",
            [
                {"type": "money", "target": "total", "amount": 2000, "current": 0,
                 "description": "Earn $2000 total"},
            ],
            {"money": 1000, "items": {}},
            prerequisite="entrepreneur"
        )
        
    def start_quest(self, quest_id):
        """Start a new quest if prerequisites are met"""
        if quest_id in self.quests:
            quest = self.quests[quest_id]
            
            # Check if already active or completed
            if quest in self.active_quests or quest in self.completed_quests:
                return False
            
            # Check prerequisite
            if quest.prerequisite:
                prereq = self.quests[quest.prerequisite]
                if prereq not in self.completed_quests or not prereq.claimed:
                    return False
            
            self.active_quests.append(quest)
            return True
        return False
    
    def update_quest(self, obj_type, target, amount=1):
        """Update progress for all active quests"""
        for quest in self.active_quests:
            quest.update_progress(obj_type, target, amount)
            
            # Auto-complete if objectives done
            if quest.is_complete() and not quest.completed:
                quest.completed = True
                return quest  # Return completed quest for notification
        return None
    
    def claim_reward(self, quest):
        """Claim quest rewards"""
        if quest.completed and not quest.claimed:
            quest.claimed = True
            self.active_quests.remove(quest)
            self.completed_quests.append(quest)
            
            # Check for new quests that can be started
            self.check_new_quests()
            
            return quest.rewards
        return None
    
    def check_new_quests(self):
        """Check if any new quests can be started"""
        for quest_id, quest in self.quests.items():
            if quest not in self.active_quests and quest not in self.completed_quests:
                # Check if prerequisite is met
                if quest.prerequisite:
                    prereq = self.quests[quest.prerequisite]
                    if prereq.claimed:
                        self.start_quest(quest_id)
                else:
                    self.start_quest(quest_id)
    
    def toggle_quest_tab(self):
        """Toggle quest UI"""
        self.show_quest_tab = not self.show_quest_tab
        
    def handle_click(self, pos, screen_width, screen_height, player, inventory):
        """Handle clicks on quest UI"""
        if not self.show_quest_tab:
            return None
        
        panel_width = min(700, screen_width - 40)
        panel_height = min(600, screen_height - 40)
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2
        
        # Check quest list clicks
        list_width = 280
        list_x = panel_x + 20
        list_y = panel_y + 70
        
        y_offset = 0
        for quest in self.active_quests:
            quest_rect = pygame.Rect(list_x, list_y + y_offset, list_width, 60)
            if quest_rect.collidepoint(pos):
                self.selected_quest = quest
                return None
            y_offset += 70
        
        # Check claim button
        if self.selected_quest and self.selected_quest.completed:
            button_x = panel_x + panel_width - 140
            button_y = panel_y + panel_height - 70
            claim_rect = pygame.Rect(button_x, button_y, 120, 40)
            
            if claim_rect.collidepoint(pos):
                rewards = self.claim_reward(self.selected_quest)
                if rewards:
                    # Give rewards
                    if "money" in rewards:
                        player.money += rewards["money"]
                    if "items" in rewards:
                        for item, count in rewards["items"].items():
                            inventory.add_item(item, count)
                    
                    self.selected_quest = None
                    return f"Quest completed! Rewards claimed!"
        
        return None
    
    def draw_quest_notification(self, quest, surface, screen_width, screen_height):
        """Draw quest completion notification"""
        if quest and quest.completed and not quest.claimed:
            # Background
            notif_width = 350
            notif_height = 80
            notif_x = (screen_width - notif_width) // 2
            notif_y = 100
            
            bg = pygame.Surface((notif_width, notif_height))
            bg.set_alpha(240)
            bg.fill((40, 80, 40))
            surface.blit(bg, (notif_x, notif_y))
            
            # Border with glow effect
            pygame.draw.rect(surface, (100, 255, 100), 
                           (notif_x, notif_y, notif_width, notif_height), 3)
            
            # Title
            title = self.title_font.render("Quest Complete!", True, (255, 255, 100))
            surface.blit(title, (notif_x + 20, notif_y + 15))
            
            # Quest name
            name = self.font.render(quest.title, True, WHITE)
            surface.blit(name, (notif_x + 20, notif_y + 45))
    
    def draw_quest_tab(self, surface, screen_width, screen_height):
        """Draw quest tab UI"""
        if not self.show_quest_tab:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Main panel
        panel_width = min(700, screen_width - 40)
        panel_height = min(600, screen_height - 40)
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2
        
        bg = pygame.Surface((panel_width, panel_height))
        bg.fill((40, 40, 40))
        surface.blit(bg, (panel_x, panel_y))
        
        pygame.draw.rect(surface, (255, 215, 0), 
                        (panel_x, panel_y, panel_width, panel_height), 3)
        
        # Title
        title = self.title_font.render("Quest Log", True, (255, 215, 0))
        surface.blit(title, (panel_x + 20, panel_y + 15))
        
        # Close hint
        close_text = self.font.render("Press Q to close", True, GRAY)
        surface.blit(close_text, (panel_x + panel_width - 150, panel_y + 15))
        
        # Stats
        stats_text = self.small_font.render(
            f"Active: {len(self.active_quests)} | Completed: {len(self.completed_quests)}",
            True, WHITE
        )
        surface.blit(stats_text, (panel_x + 20, panel_y + 45))
        
        # Divider line
        pygame.draw.line(surface, GRAY, 
                        (panel_x + 20, panel_y + 65),
                        (panel_x + panel_width - 20, panel_y + 65), 2)
        
        # Quest list (left side)
        list_width = 280
        list_x = panel_x + 20
        list_y = panel_y + 70
        
        list_label = self.font.render("Active Quests", True, YELLOW)
        surface.blit(list_label, (list_x, list_y))
        
        # Draw quest items
        y_offset = 30
        for quest in self.active_quests:
            quest_y = list_y + y_offset
            is_selected = quest == self.selected_quest
            
            # Quest box
            quest_rect = pygame.Rect(list_x, quest_y, list_width, 60)
            color = (80, 80, 80) if is_selected else (60, 60, 60)
            if quest.completed:
                color = (80, 120, 80) if is_selected else (60, 100, 60)
            
            pygame.draw.rect(surface, color, quest_rect)
            pygame.draw.rect(surface, YELLOW if is_selected else GRAY, quest_rect, 2)
            
            # Quest title
            title_text = self.font.render(quest.title, True, WHITE)
            surface.blit(title_text, (quest_rect.x + 10, quest_rect.y + 8))
            
            # Completion status
            if quest.completed:
                status = self.small_font.render("✓ Complete!", True, (100, 255, 100))
            else:
                completed = sum(1 for obj in quest.objectives if obj["current"] >= obj["amount"])
                total = len(quest.objectives)
                status = self.small_font.render(
                    f"Progress: {completed}/{total}",
                    True, GRAY
                )
            surface.blit(status, (quest_rect.x + 10, quest_rect.y + 35))
            
            y_offset += 70
        
        # No active quests message
        if not self.active_quests:
            no_quests = self.font.render("No active quests", True, GRAY)
            surface.blit(no_quests, (list_x + 60, list_y + 50))
        
        # Vertical divider
        divider_x = panel_x + 320
        pygame.draw.line(surface, GRAY,
                        (divider_x, panel_y + 70),
                        (divider_x, panel_y + panel_height - 20), 2)
        
        # Quest details (right side)
        detail_x = divider_x + 20
        detail_y = panel_y + 70
        
        if self.selected_quest:
            quest = self.selected_quest
            
            # Title
            detail_title = self.title_font.render(quest.title, True, YELLOW)
            surface.blit(detail_title, (detail_x, detail_y))
            
            # Description
            desc_y = detail_y + 40
            desc_text = self.font.render(quest.description, True, WHITE)
            surface.blit(desc_text, (detail_x, desc_y))
            
            # Objectives
            obj_y = desc_y + 40
            obj_label = self.font.render("Objectives:", True, YELLOW)
            surface.blit(obj_label, (detail_x, obj_y))
            
            obj_y += 30
            for line in quest.get_progress_text():
                obj_text = self.small_font.render(line, True, WHITE)
                surface.blit(obj_text, (detail_x + 10, obj_y))
                obj_y += 25
            
            # Rewards
            reward_y = obj_y + 20
            reward_label = self.font.render("Rewards:", True, YELLOW)
            surface.blit(reward_label, (detail_x, reward_y))
            
            reward_y += 30
            if "money" in quest.rewards:
                money_text = self.small_font.render(
                    f"💰 ${quest.rewards['money']}",
                    True, (255, 215, 0)
                )
                surface.blit(money_text, (detail_x + 10, reward_y))
                reward_y += 25
            
            if "items" in quest.rewards:
                for item, count in quest.rewards["items"].items():
                    item_name = item.replace("_", " ").title()
                    item_text = self.small_font.render(
                        f"📦 {count}x {item_name}",
                        True, WHITE
                    )
                    surface.blit(item_text, (detail_x + 10, reward_y))
                    reward_y += 25
            
            # Claim button
            if quest.completed and not quest.claimed:
                button_x = panel_x + panel_width - 140
                button_y = panel_y + panel_height - 70
                claim_rect = pygame.Rect(button_x, button_y, 120, 40)
                
                pygame.draw.rect(surface, (80, 150, 80), claim_rect)
                pygame.draw.rect(surface, (100, 255, 100), claim_rect, 3)
                
                claim_text = self.font.render("CLAIM", True, WHITE)
                claim_x = claim_rect.centerx - claim_text.get_width() // 2
                claim_y = claim_rect.centery - claim_text.get_height() // 2
                surface.blit(claim_text, (claim_x, claim_y))
        else:
            # No quest selected
            no_select = self.font.render("Select a quest to view details", True, GRAY)
            surface.blit(no_select, (detail_x, detail_y + 50))
    
    def save_data(self):
        """Return data for saving"""
        return {
            "active": [q.id for q in self.active_quests],
            "completed": [q.id for q in self.completed_quests],
            "progress": {
                quest.id: [
                    {"current": obj["current"]} for obj in quest.objectives
                ]
                for quest in self.active_quests
            }
        }
    
    def load_data(self, data):
        """Load saved data"""
        if "active" in data:
            self.active_quests = []
            for quest_id in data["active"]:
                if quest_id in self.quests:
                    self.active_quests.append(self.quests[quest_id])
        
        if "completed" in data:
            self.completed_quests = []
            for quest_id in data["completed"]:
                if quest_id in self.quests:
                    quest = self.quests[quest_id]
                    quest.completed = True
                    quest.claimed = True
                    self.completed_quests.append(quest)
        
        if "progress" in data:
            for quest_id, progress_list in data["progress"].items():
                if quest_id in self.quests:
                    quest = self.quests[quest_id]
                    for i, progress in enumerate(progress_list):
                        if i < len(quest.objectives):
                            quest.objectives[i]["current"] = progress["current"]
