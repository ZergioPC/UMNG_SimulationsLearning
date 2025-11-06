import numpy as np
from typing import List, Tuple


class ChainLink:
    """Represents a single point/particle in the chain."""
    
    def __init__(self, position: np.ndarray, mass: float = 1.0, fixed: bool = False):
        """
        Initialize a chain link.
        
        Args:
            position: 3D position vector [x, y, z]
            mass: Mass of the link
            fixed: Whether this link is fixed in space (e.g., anchor point)
        """
        self.position = np.array(position, dtype=np.float64)
        self.prev_position = np.array(position, dtype=np.float64)
        self.velocity = np.zeros(3, dtype=np.float64)
        self.acceleration = np.zeros(3, dtype=np.float64)
        self.force = np.zeros(3, dtype=np.float64)
        self.mass = mass
        self.fixed = fixed
    
    def apply_force(self, force: np.ndarray):
        """Add a force to this link."""
        if not self.fixed:
            self.force += force
    
    def clear_forces(self):
        """Reset accumulated forces."""
        self.force = np.zeros(3, dtype=np.float64)
    
    def update_acceleration(self):
        """Calculate acceleration from forces (F = ma)."""
        if not self.fixed and self.mass > 0:
            self.acceleration = self.force / self.mass
        else:
            self.acceleration = np.zeros(3, dtype=np.float64)


class Chain:
    """Manages a chain made of connected links."""
    
    def __init__(self, start_position: np.ndarray, num_links: int, 
                 link_length: float, link_mass: float = 1.0):
        """
        Create a chain.
        
        Args:
            start_position: Starting position of the chain [x, y, z]
            num_links: Number of links in the chain
            link_length: Distance between adjacent links
            link_mass: Mass of each link
        """
        self.links: List[ChainLink] = []
        self.link_length = link_length
        self.num_links = num_links
        
        # Create links hanging vertically downward from start position
        for i in range(num_links):
            position = start_position + np.array([0, 0, -i * link_length])
            is_fixed = (i == 0)  # First link is fixed (anchor point)
            link = ChainLink(position, mass=link_mass, fixed=is_fixed)
            self.links.append(link)
        
        # Store connections (pairs of linked indices)
        self.connections: List[Tuple[int, int]] = []
        for i in range(num_links - 1):
            self.connections.append((i, i + 1))
    
    def apply_gravity(self, gravity: np.ndarray = np.array([0, 0, -9.81])):
        """Apply gravitational force to all links."""
        for link in self.links:
            if not link.fixed:
                link.apply_force(gravity * link.mass)
    
    def apply_wind(self, wind_force: np.ndarray):
        """Apply wind force to all links."""
        for link in self.links:
            if not link.fixed:
                link.apply_force(wind_force)
    
    def get_positions(self) -> np.ndarray:
        """Get all link positions as a numpy array."""
        return np.array([link.position for link in self.links])
    
    def get_connection_pairs(self) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Get pairs of connected positions for rendering."""
        pairs = []
        for i, j in self.connections:
            pairs.append((self.links[i].position, self.links[j].position))
        return pairs
    
    def set_fixed(self, index: int, fixed: bool):
        """Fix or unfix a specific link."""
        if 0 <= index < len(self.links):
            self.links[index].fixed = fixed
    
    def get_total_energy(self) -> float:
        """Calculate total kinetic + potential energy of the chain."""
        kinetic = 0.0
        potential = 0.0
        
        for link in self.links:
            if not link.fixed:
                # Kinetic energy: 0.5 * m * v^2
                v_squared = np.dot(link.velocity, link.velocity)
                kinetic += 0.5 * link.mass * v_squared
                
                # Potential energy: m * g * h (assuming gravity = -9.81 in z)
                potential += link.mass * 9.81 * link.position[2]
        
        return kinetic + potential
    
    def reset(self, start_position: np.ndarray):
        """Reset chain to initial configuration."""
        for i, link in enumerate(self.links):
            position = start_position + np.array([0, 0, -i * self.link_length])
            link.position = np.array(position, dtype=np.float64)
            link.prev_position = np.array(position, dtype=np.float64)
            link.velocity = np.zeros(3, dtype=np.float64)
            link.acceleration = np.zeros(3, dtype=np.float64)
            link.clear_forces()