# plot_system.py
import pygame
from settings import *

class PlotSystem:
    """Manages farmable plot claiming, selling, and locking"""
    
    def __init__(self):
        self.claimed_plots = set()  # Set of (grid_x, grid_y) tuples
        self.locked_plots = set()  # Set of locked plots that can't be sold
        self.claim_cost = 50  # Cost to claim a plot
        self.sell_value = int(self.claim_cost * 0.8)  # 80% refund
        self.font = pygame.font.Font(None, 18)
        self.small_font = pygame.font.Font(None, 14)
        
    def is_claimed(self, grid_pos):
        """Check if a plot is claimed"""
        return grid_pos in self.claimed_plots
    
    def is_locked(self, grid_pos):
        """Check if a plot is locked"""
        return grid_pos in self.locked_plots
    
    def can_claim(self, grid_pos, world, player):
        """Check if a position can be claimed - ONLY with hoe equipped"""
        # Must have hoe equipped to claim plots
        if player.current_tool != "hoe":
            return False
            
        tile = world.tile_map.get(grid_pos)
        if not tile:
            return False
        
        # Only grass tiles can be claimed
        return tile.kind == "G" and grid_pos not in self.claimed_plots
    
    def can_sell(self, grid_pos, world):
        """Check if a plot can be sold"""
        if grid_pos not in self.claimed_plots:
            return False, "Plot not claimed!"
        
        if grid_pos in self.locked_plots:
            return False, "Plot is locked! Unlock first (L key)"
        
        # Check if there's a crop on this plot
        tile_pos = (grid_pos[0] * TILE_SIZE, grid_pos[1] * TILE_SIZE)
        for crop in world.crops:
            if crop.rect.topleft == tile_pos:
                return False, "Remove crops first!"
        
        # Check if tile is tilled
        tile = world.tile_map.get(grid_pos)
        if tile and tile.kind == "S":
            return False, "Tile is tilled! Can't sell."
        
        return True, ""
    
    def claim_plot(self, grid_pos, player, world):
        """Attempt to claim a plot - ONLY with hoe equipped"""
        # Check if hoe is equipped first
        if player.current_tool != "hoe":
            return False, "Must have HOE equipped to claim plots! (Press T)"
        
        if not self.can_claim(grid_pos, world, player):
            return False, "Cannot claim this tile!"
        
        if player.money < self.claim_cost:
            return False, f"Need ${self.claim_cost} to claim plot!"
        
        # Deduct money and claim plot
        player.money -= self.claim_cost
        self.claimed_plots.add(grid_pos)
        return True, f"Plot claimed! (-${self.claim_cost})"
    
    def sell_plot(self, grid_pos, player, world):
        """Sell a claimed plot for 80% of claim cost"""
        can_sell, message = self.can_sell(grid_pos, world)
        
        if not can_sell:
            return False, message
        
        # Remove from claimed plots and give money back
        self.claimed_plots.remove(grid_pos)
        
        # Also remove from locked plots if it was locked
        if grid_pos in self.locked_plots:
            self.locked_plots.remove(grid_pos)
        
        player.money += self.sell_value
        return True, f"Plot sold! (+${self.sell_value})"
    
    def toggle_lock(self, grid_pos):
        """Toggle lock status of a plot"""
        if grid_pos not in self.claimed_plots:
            return False, "Plot not claimed!"
        
        if grid_pos in self.locked_plots:
            self.locked_plots.remove(grid_pos)
            return True, "Plot unlocked!"
        else:
            self.locked_plots.add(grid_pos)
            return True, "Plot locked!"
    
    def get_connected_plots(self):
        """Group claimed plots into connected regions for outline drawing"""
        if not self.claimed_plots:
            return []
        
        visited = set()
        regions = []
        
        for plot in self.claimed_plots:
            if plot in visited:
                continue
            
            # BFS to find connected region
            region = set()
            queue = [plot]
            
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                
                visited.add(current)
                region.add(current)
                
                # Check 4 neighbors
                x, y = current
                neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                
                for neighbor in neighbors:
                    if neighbor in self.claimed_plots and neighbor not in visited:
                        queue.append(neighbor)
            
            regions.append(region)
        
        return regions
    
    def draw_claimed_indicators(self, surface):
        """Draw visual indicators for claimed plots with connected outlines"""
        regions = self.get_connected_plots()
        
        for region in regions:
            # Draw outline for each connected region
            outline_color = (255, 215, 0)  # Gold
            
            for grid_x, grid_y in region:
                x = grid_x * TILE_SIZE
                y = grid_y * TILE_SIZE
                
                # Draw lock icon if plot is locked
                if (grid_x, grid_y) in self.locked_plots:
                    lock_surface = pygame.Surface((12, 12), pygame.SRCALPHA)
                    # Lock body
                    pygame.draw.rect(lock_surface, (255, 215, 0), (2, 5, 8, 6))
                    # Lock shackle
                    pygame.draw.arc(lock_surface, (255, 215, 0), (3, 1, 6, 6), 0, 3.14159, 2)
                    # Draw lock in corner of tile
                    surface.blit(lock_surface, (x + 2, y + 2))
                
                # Check each edge to see if it should be drawn
                # Top edge
                if (grid_x, grid_y - 1) not in region:
                    pygame.draw.line(surface, outline_color, 
                                   (x, y), (x + TILE_SIZE, y), 2)
                
                # Bottom edge
                if (grid_x, grid_y + 1) not in region:
                    pygame.draw.line(surface, outline_color, 
                                   (x, y + TILE_SIZE), (x + TILE_SIZE, y + TILE_SIZE), 2)
                
                # Left edge
                if (grid_x - 1, grid_y) not in region:
                    pygame.draw.line(surface, outline_color, 
                                   (x, y), (x, y + TILE_SIZE), 2)
                
                # Right edge
                if (grid_x + 1, grid_y) not in region:
                    pygame.draw.line(surface, outline_color, 
                                   (x + TILE_SIZE, y), (x + TILE_SIZE, y + TILE_SIZE), 2)
    
    def draw_claimable_hint(self, surface, mouse_pos, world, player):
        """Draw hint when hovering over claimable plot - ONLY when hoe is equipped"""
        grid_x = mouse_pos[0] // TILE_SIZE
        grid_y = mouse_pos[1] // TILE_SIZE
        grid_pos = (grid_x, grid_y)
        
        x = grid_x * TILE_SIZE
        y = grid_y * TILE_SIZE
        
        # Check if plot is claimed and can be sold
        if grid_pos in self.claimed_plots:
            can_sell, sell_message = self.can_sell(grid_pos, world)
            is_locked = grid_pos in self.locked_plots
            
            # Draw highlight
            highlight = pygame.Surface((TILE_SIZE, TILE_SIZE))
            highlight.set_alpha(80)
            if is_locked:
                highlight.fill((255, 165, 0))  # Orange for locked
            elif can_sell:
                highlight.fill((255, 100, 100))  # Red for sellable
            else:
                highlight.fill((150, 150, 150))  # Gray for not sellable
            surface.blit(highlight, (x, y))
            
            # Draw prompt
            if can_sell:
                text = self.font.render(f"Right-click: Sell (+${self.sell_value}) | L: Lock", True, WHITE)
            elif is_locked:
                text = self.font.render(f"L: Unlock plot", True, WHITE)
            else:
                text = self.font.render(sell_message, True, RED)
            
            # Position above tile
            text_x = x + TILE_SIZE // 2 - text.get_width() // 2
            text_y = y - 25
            
            # Background
            bg = pygame.Surface((text.get_width() + 8, text.get_height() + 4))
            bg.set_alpha(200)
            bg.fill((40, 40, 40))
            surface.blit(bg, (text_x - 4, text_y - 2))
            
            surface.blit(text, (text_x, text_y))
            
        # Check if plot can be claimed (only when hoe equipped)
        elif player.current_tool == "hoe" and self.can_claim(grid_pos, world, player):
            # Draw highlight
            highlight = pygame.Surface((TILE_SIZE, TILE_SIZE))
            highlight.set_alpha(80)
            highlight.fill((255, 255, 100))
            surface.blit(highlight, (x, y))
            
            # Draw claim prompt
            can_afford = player.money >= self.claim_cost
            color = WHITE if can_afford else RED
            text = self.font.render(f"Right-click: Claim (${self.claim_cost})", True, color)
            
            # Position above tile
            text_x = x + TILE_SIZE // 2 - text.get_width() // 2
            text_y = y - 20
            
            # Background
            bg = pygame.Surface((text.get_width() + 8, text.get_height() + 4))
            bg.set_alpha(200)
            bg.fill((40, 40, 40))
            surface.blit(bg, (text_x - 4, text_y - 2))
            
            surface.blit(text, (text_x, text_y))
    
    def save_data(self):
        """Return data for saving"""
        return {
            "claimed_plots": list(self.claimed_plots),
            "locked_plots": list(self.locked_plots)
        }
    
    def load_data(self, data):
        """Load saved data"""
        if "claimed_plots" in data:
            self.claimed_plots = set(tuple(pos) for pos in data["claimed_plots"])
        if "locked_plots" in data:
            self.locked_plots = set(tuple(pos) for pos in data["locked_plots"])
