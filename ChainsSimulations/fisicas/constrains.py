import numpy as np
from typing import List, Tuple
from ChainsSimulations.fisicas.cadenas import Chain, ChainLink


class DistanceConstraint:
    """Represents a distance constraint between two chain links."""
    
    def __init__(self, link_a: ChainLink, link_b: ChainLink, rest_length: float):
        """
        Initialize a distance constraint.
        
        Args:
            link_a: First link
            link_b: Second link
            rest_length: Desired distance between links
        """
        self.link_a = link_a
        self.link_b = link_b
        self.rest_length = rest_length
    
    def solve(self, stiffness: float = 1.0):
        """
        Solve the constraint by adjusting link positions.
        
        Args:
            stiffness: Constraint stiffness (0.0 to 1.0)
                      1.0 = rigid, lower values = more elastic
        """
        # Calculate current distance vector
        delta = self.link_b.position - self.link_a.position
        current_distance = np.linalg.norm(delta)
        
        # Avoid division by zero
        if current_distance < 1e-6:
            return
        
        # Calculate correction
        difference = (current_distance - self.rest_length) / current_distance
        correction = delta * difference * stiffness * 0.5
        
        # Apply correction based on whether links are fixed
        if not self.link_a.fixed and not self.link_b.fixed:
            # Both links can move - split correction equally
            self.link_a.position += correction
            self.link_b.position -= correction
        elif not self.link_a.fixed:
            # Only link_a can move
            self.link_a.position += correction * 2.0
        elif not self.link_b.fixed:
            # Only link_b can move
            self.link_b.position -= correction * 2.0
        # If both are fixed, do nothing


class ConstraintSolver:
    """Manages and solves all constraints in the simulation."""
    
    def __init__(self, iterations: int = 10, stiffness: float = 1.0):
        """
        Initialize the constraint solver.
        
        Args:
            iterations: Number of solver iterations per step
            stiffness: Global constraint stiffness (0.0 to 1.0)
        """
        self.constraints: List[DistanceConstraint] = []
        self.iterations = iterations
        self.stiffness = stiffness
    
    def add_constraint(self, constraint: DistanceConstraint):
        """Add a constraint to the solver."""
        self.constraints.append(constraint)
    
    def create_chain_constraints(self, chain: Chain):
        """
        Create distance constraints for all connections in a chain.
        
        Args:
            chain: Chain object to create constraints for
        """
        self.constraints.clear()
        
        for i, j in chain.connections:
            constraint = DistanceConstraint(
                chain.links[i],
                chain.links[j],
                chain.link_length
            )
            self.constraints.append(constraint)
    
    def solve(self):
        """Solve all constraints iteratively."""
        for _ in range(self.iterations):
            for constraint in self.constraints:
                constraint.solve(self.stiffness)
    
    def set_iterations(self, iterations: int):
        """Update the number of solver iterations."""
        self.iterations = max(1, iterations)
    
    def set_stiffness(self, stiffness: float):
        """Update the global stiffness parameter."""
        self.stiffness = np.clip(stiffness, 0.0, 1.0)
    
    def clear_constraints(self):
        """Remove all constraints."""
        self.constraints.clear()


class CollisionConstraint:
    """Handles collision constraints (e.g., ground plane, spheres)."""
    
    @staticmethod
    def apply_ground_collision(link: ChainLink, ground_height: float = 0.0, 
                               restitution: float = 0.5):
        """
        Apply ground plane collision constraint.
        
        Args:
            link: Chain link to check
            ground_height: Height of the ground plane
            restitution: Bounce coefficient (0.0 = no bounce, 1.0 = perfect bounce)
        """
        if link.fixed:
            return
        
        if link.position[2] < ground_height:
            # Position correction
            link.position[2] = ground_height
            
            # Velocity reflection with restitution
            if link.velocity[2] < 0:
                link.velocity[2] *= -restitution
                
                # Apply friction to horizontal velocity
                friction = 0.9
                link.velocity[0] *= friction
                link.velocity[1] *= friction
    
    @staticmethod
    def apply_sphere_collision(link: ChainLink, sphere_center: np.ndarray,
                               sphere_radius: float, restitution: float = 0.5):
        """
        Apply sphere collision constraint.
        
        Args:
            link: Chain link to check
            sphere_center: Center position of the sphere
            sphere_radius: Radius of the sphere
            restitution: Bounce coefficient
        """
        if link.fixed:
            return
        
        # Calculate distance from sphere center
        delta = link.position - sphere_center
        distance = np.linalg.norm(delta)
        
        if distance < sphere_radius and distance > 1e-6:
            # Push link outside the sphere
            normal = delta / distance
            penetration = sphere_radius - distance
            link.position += normal * penetration
            
            # Reflect velocity
            velocity_normal = np.dot(link.velocity, normal)
            if velocity_normal < 0:
                link.velocity -= normal * velocity_normal * (1.0 + restitution)


class AdvancedConstraintSolver(ConstraintSolver):
    """Extended constraint solver with collision handling."""
    
    def __init__(self, iterations: int = 10, stiffness: float = 1.0):
        super().__init__(iterations, stiffness)
        self.ground_enabled = False
        self.ground_height = 0.0
        self.ground_restitution = 0.5
        self.collision_spheres: List[Tuple[np.ndarray, float]] = []
    
    def enable_ground(self, height: float = 0.0, restitution: float = 0.5):
        """Enable ground plane collision."""
        self.ground_enabled = True
        self.ground_height = height
        self.ground_restitution = restitution
    
    def disable_ground(self):
        """Disable ground plane collision."""
        self.ground_enabled = False
    
    def add_collision_sphere(self, center: np.ndarray, radius: float):
        """Add a sphere obstacle."""
        self.collision_spheres.append((np.array(center), radius))
    
    def clear_collision_spheres(self):
        """Remove all sphere obstacles."""
        self.collision_spheres.clear()
    
    def solve_with_collisions(self, chain: Chain):
        """Solve constraints and apply collision constraints."""
        # Solve distance constraints
        self.solve()
        
        # Apply collision constraints
        for link in chain.links:
            if self.ground_enabled:
                CollisionConstraint.apply_ground_collision(
                    link, self.ground_height, self.ground_restitution
                )
            
            for center, radius in self.collision_spheres:
                CollisionConstraint.apply_sphere_collision(
                    link, center, radius, 0.5
                )