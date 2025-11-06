"""
Main application for chain physics simulation.
Integrates physics calculations with Panda3D rendering.
"""

import numpy as np
from ChainsSimulations.fisicas.cadenas import Chain
from ChainsSimulations.fisicas.constrains import AdvancedConstraintSolver
from ChainsSimulations.render.panda_renderer import PandaRenderer
from panda3d.core import Vec3


class ChainSimulation:
    """Main simulation class integrating physics and rendering."""
    
    def __init__(self):
        """Initialize the simulation."""
        # Simulation parameters
        self.num_links = 7
        self.link_length = 0.5
        self.link_mass = 1.0
        self.start_position = np.array([0.0, 0.0, 5.0])
        
        # Physics components
        self.chain = Chain(
            start_position=self.start_position,
            num_links=self.num_links,
            link_length=self.link_length,
            link_mass=self.link_mass
        )
        
        # Constraint solver with collision support
        self.solver = AdvancedConstraintSolver(
            iterations=10,
            stiffness=1.0
        )
        self.solver.create_chain_constraints(self.chain)
        self.solver.enable_ground(height=0.0, restitution=0.3)
        
        # Physics settings
        self.gravity = np.array([0.0, 0.0, -9.81])
        self.damping = 0.99  # Velocity damping (air resistance)
        self.substeps = 5  # Physics substeps per frame
        
        # Rendering
        self.renderer = PandaRenderer()
        self.renderer.create_chain_visualization(self.chain, link_radius=0.15)
        self.renderer.create_ground_plane(height=0.0, size=20.0)
        
        # Setup camera controls
        self.renderer.setup_camera_controls(target_pos=Vec3(0, 0, 2))
        
        # Info text
        self.info_text = self.renderer.add_text_info("", position=(0.02, 0.98))
        
        # Simulation state
        self.paused = False
        self.time_elapsed = 0.0
        
        # Setup keyboard controls
        self.setup_controls()
        
        # Set physics callback
        self.renderer.set_physics_callback(self.update_physics)
    
    def setup_controls(self):
        """Setup keyboard controls for the simulation."""
        self.renderer.accept("space", self.toggle_pause)
        self.renderer.accept("r", self.reset_simulation)
        self.renderer.accept("g", self.toggle_ground)
        self.renderer.accept("w", self.apply_wind_impulse)
        self.renderer.accept("escape", self.renderer.userExit)
        
        # Adjust physics parameters
        self.renderer.accept("arrow_up", self.increase_iterations)
        self.renderer.accept("arrow_down", self.decrease_iterations)
        self.renderer.accept("+", self.increase_stiffness)
        self.renderer.accept("-", self.decrease_stiffness)
    
    def toggle_pause(self):
        """Toggle simulation pause."""
        self.paused = not self.paused
        status = "PAUSED" if self.paused else "RUNNING"
        print(f"Simulation {status}")
    
    def reset_simulation(self):
        """Reset the simulation to initial state."""
        self.chain.reset(self.start_position)
        self.time_elapsed = 0.0
        print("Simulation reset")
    
    def toggle_ground(self):
        """Toggle ground collision."""
        if self.solver.ground_enabled:
            self.solver.disable_ground()
            print("Ground disabled")
        else:
            self.solver.enable_ground(height=0.0, restitution=0.3)
            print("Ground enabled")
    
    def apply_wind_impulse(self):
        """Apply a wind impulse to the chain."""
        wind = np.array([50.0, 0.0, 0.0])
        self.chain.apply_wind(wind)
        print("Wind impulse applied")
    
    def increase_iterations(self):
        """Increase constraint solver iterations."""
        self.solver.set_iterations(self.solver.iterations + 1)
        print(f"Solver iterations: {self.solver.iterations}")
    
    def decrease_iterations(self):
        """Decrease constraint solver iterations."""
        self.solver.set_iterations(max(1, self.solver.iterations - 1))
        print(f"Solver iterations: {self.solver.iterations}")
    
    def increase_stiffness(self):
        """Increase constraint stiffness."""
        new_stiffness = min(1.0, self.solver.stiffness + 0.1)
        self.solver.set_stiffness(new_stiffness)
        print(f"Stiffness: {self.solver.stiffness:.2f}")
    
    def decrease_stiffness(self):
        """Decrease constraint stiffness."""
        new_stiffness = max(0.1, self.solver.stiffness - 0.1)
        self.solver.set_stiffness(new_stiffness)
        print(f"Stiffness: {self.solver.stiffness:.2f}")
    
    def verlet_integration(self, dt: float):
        """
        Perform Verlet integration for physics simulation.
        
        Args:
            dt: Time step
        """
        for link in self.chain.links:
            if not link.fixed:
                # Calculate acceleration from forces
                link.update_acceleration()
                
                # Verlet integration
                # Store current position
                current_pos = link.position.copy()
                
                # Update position: x(t+dt) = 2*x(t) - x(t-dt) + a*dt²
                link.position = (2.0 * link.position - link.prev_position + 
                                link.acceleration * dt * dt)
                
                # Apply damping
                link.position += (link.position - link.prev_position) * (self.damping - 1.0)
                
                # Update velocity for external use: v = (x(t) - x(t-dt)) / dt
                link.velocity = (link.position - link.prev_position) / dt
                
                # Store previous position
                link.prev_position = current_pos
                
                # Clear forces for next iteration
                link.clear_forces()
    
    def update_physics(self, dt: float):
        """
        Main physics update function called each frame.
        
        Args:
            dt: Delta time since last frame
        """
        if self.paused:
            return
        
        # Limit dt to avoid instability
        dt = min(dt, 0.033)  # Cap at ~30 FPS
        
        # Physics substeps for stability
        substep_dt = dt / self.substeps
        
        for _ in range(self.substeps):
            # Apply forces
            self.chain.apply_gravity(self.gravity)
            
            # Integrate physics
            self.verlet_integration(substep_dt)
            
            # Solve constraints (distance + collisions)
            self.solver.solve_with_collisions(self.chain)
        
        # Update visualization
        self.renderer.update_chain_visualization(self.chain)
        
        # Update time
        self.time_elapsed += dt
        
        # Update info text
        energy = self.chain.get_total_energy()
        self.info_text.setText(
            f"Time: {self.time_elapsed:.2f}s | "
            f"Energy: {energy:.2f}J | "
            f"Iterations: {self.solver.iterations} | "
            f"Stiffness: {self.solver.stiffness:.2f}\n"
            f"Controls: SPACE=Pause, R=Reset, G=Ground, W=Wind, ESC=Exit\n"
            f"Arrows=Iterations, +/-=Stiffness"
        )
    
    def run(self):
        """Start the simulation."""
        print("=" * 60)
        print("CHAIN PHYSICS SIMULATION")
        print("=" * 60)
        print(f"Links: {self.num_links}")
        print(f"Link length: {self.link_length}m")
        print(f"Link mass: {self.link_mass}kg")
        print(f"Solver iterations: {self.solver.iterations}")
        print(f"Substeps: {self.substeps}")
        print("=" * 60)
        print("CONTROLS:")
        print("  SPACE       - Pause/Resume")
        print("  R           - Reset simulation")
        print("  G           - Toggle ground collision")
        print("  W           - Apply wind impulse")
        print("  Arrow Up    - Increase solver iterations")
        print("  Arrow Down  - Decrease solver iterations")
        print("  +           - Increase stiffness")
        print("  -           - Decrease stiffness")
        print("  Mouse drag  - Rotate camera")
        print("  Mouse wheel - Zoom in/out")
        print("  ESC         - Exit")
        print("=" * 60)
        
        # Run Panda3D main loop
        self.renderer.run()


def main():
    """Entry point for the application."""
    simulation = ChainSimulation()
    simulation.run()


if __name__ == "__main__":
    main()