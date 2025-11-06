"""
Panda3D rendering module for chain physics visualization.
Handles 3D visualization of chain links and environment.
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    LineSegs, NodePath, AmbientLight, DirectionalLight,
    Vec3, Vec4, TransparencyAttrib, GeomNode, ClockObject, WindowProperties
)
from direct.task import Task
import numpy as np
from typing import List, Callable, Optional
from ChainsSimulations.fisicas.cadenas import Chain


class PandaRenderer(ShowBase):
    """Panda3D renderer for chain physics simulation."""
    
    def __init__(self):
        """
        Initialize the Panda3D renderer.
        
        Args:
            window_title: Title for the application window
        """
        super().__init__()
        
        # Window setup
        
        # Camera setup
        self.setup_camera()
        
        # Lighting setup
        self.setup_lighting()
        
        # Chain visualization nodes
        self.chain_nodes: List[NodePath] = []
        self.connection_node: Optional[NodePath] = None
        
        # Ground plane
        self.ground_node: Optional[NodePath] = None
        
        # Sphere obstacles
        self.sphere_nodes: List[NodePath] = []
        
        # Physics update callback
        self.physics_callback: Optional[Callable] = None
        
        # Performance tracking
        self.frame_count = 0
        self.fps_text = None
        
    def setup_camera(self):
        """Configure camera position and orientation."""
        self.disableMouse()
        self.camera.setPos(0, -15, 5)
        self.camera.lookAt(0, 0, 0)
        
    def setup_lighting(self):
        """Setup scene lighting."""
        # Ambient light
        ambient = AmbientLight("ambient")
        ambient.setColor(Vec4(0.4, 0.4, 0.4, 1.0))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)
        
        # Directional light
        directional = DirectionalLight("directional")
        directional.setColor(Vec4(0.8, 0.8, 0.8, 1.0))
        directional_np = self.render.attachNewNode(directional)
        directional_np.setHpr(45, -45, 0)
        self.render.setLight(directional_np)
        
    def create_chain_visualization(self, chain: Chain, link_radius: float = 0.1):
        """
        Create visual representation of chain links.
        
        Args:
            chain: Chain object to visualize
            link_radius: Visual radius of each link sphere
        """
        # Clear existing chain nodes
        self.clear_chain_visualization()
        
        # Create sphere for each link
        for i, link in enumerate(chain.links):
            sphere = self.loader.loadModel("smiley")
            sphere.setScale(link_radius)
            sphere.setPos(Vec3(*link.position))
            
            # Color: red for fixed, blue for movable
            if link.fixed:
                sphere.setColor(1.0, 0.2, 0.2, 1.0)
            else:
                sphere.setColor(0.2, 0.5, 1.0, 1.0)
            
            sphere.reparentTo(self.render)
            self.chain_nodes.append(sphere)
    
    def update_chain_visualization(self, chain: Chain):
        """
        Update positions of chain link visuals.
        
        Args:
            chain: Chain object with updated positions
        """
        for i, link in enumerate(chain.links):
            if i < len(self.chain_nodes):
                self.chain_nodes[i].setPos(Vec3(*link.position))
        
        # Update connections
        self.update_connections(chain)
    
    def update_connections(self, chain: Chain):
        """
        Draw lines between connected links.
        
        Args:
            chain: Chain object
        """
        # Remove old connection lines
        if self.connection_node:
            self.connection_node.removeNode()
        
        # Create new lines
        lines = LineSegs()
        lines.setThickness(2.0)
        lines.setColor(0.3, 0.3, 0.3, 1.0)
        
        for link_a, link_b in chain.get_connection_pairs():
            lines.moveTo(Vec3(*link_a))
            lines.drawTo(Vec3(*link_b))
        
        # Create geometry node
        node = lines.create()
        self.connection_node = self.render.attachNewNode(node)
    
    def create_ground_plane(self, height: float = 0.0, size: float = 20.0):
        """
        Create visual ground plane.
        
        Args:
            height: Height of the ground plane
            size: Size of the plane (square)
        """
        if self.ground_node:
            self.ground_node.removeNode()
        
        # Create grid lines
        lines = LineSegs()
        lines.setThickness(1.0)
        lines.setColor(0.5, 0.5, 0.5, 0.5)
        
        grid_spacing = 1.0
        grid_count = int(size / grid_spacing)
        half_size = size / 2.0
        
        # Draw grid
        for i in range(grid_count + 1):
            offset = -half_size + i * grid_spacing
            
            # Lines parallel to X
            lines.moveTo(Vec3(-half_size, offset, height))
            lines.drawTo(Vec3(half_size, offset, height))
            
            # Lines parallel to Y
            lines.moveTo(Vec3(offset, -half_size, height))
            lines.drawTo(Vec3(offset, half_size, height))
        
        node = lines.create()
        self.ground_node = self.render.attachNewNode(node)
        self.ground_node.setTransparency(TransparencyAttrib.MAlpha)
    
    def create_sphere_obstacle(self, center: np.ndarray, radius: float):
        """
        Create visual sphere obstacle.
        
        Args:
            center: Center position of sphere
            radius: Radius of sphere
        """
        sphere = self.loader.loadModel("models/sphere")
        sphere.setScale(radius)
        sphere.setPos(Vec3(*center))
        sphere.setColor(1.0, 0.8, 0.2, 0.6)
        sphere.setTransparency(TransparencyAttrib.MAlpha)
        sphere.reparentTo(self.render)
        self.sphere_nodes.append(sphere)
    
    def clear_sphere_obstacles(self):
        """Remove all sphere obstacle visuals."""
        for sphere in self.sphere_nodes:
            sphere.removeNode()
        self.sphere_nodes.clear()
    
    def clear_chain_visualization(self):
        """Remove all chain visual nodes."""
        for node in self.chain_nodes:
            node.removeNode()
        self.chain_nodes.clear()
        
        if self.connection_node:
            self.connection_node.removeNode()
            self.connection_node = None
    
    def set_physics_callback(self, callback: Callable):
        """
        Set the physics update callback function.
        
        Args:
            callback: Function to call each frame for physics update
        """
        self.physics_callback = callback
        self.taskMgr.add(self.update_task, "physics_update")
    
    def update_task(self, task: Task):
        """
        Main update loop task.
        
        Args:
            task: Panda3D task object
        """
        if self.physics_callback:
            globalClock = ClockObject.getGlobalClock()
            dt = globalClock.getDt()
            self.physics_callback(dt)
        
        return Task.cont
    
    def setup_camera_controls(self, target_pos: Vec3 = Vec3(0, 0, 0)):
        """
        Setup simple camera controls.
        
        Args:
            target_pos: Position the camera should look at
        """
        self.camera_target = target_pos
        self.camera_distance = 15.0
        self.camera_angle_h = 0.0
        self.camera_angle_v = 20.0
        
        # Mouse drag for camera rotation
        self.accept("mouse1", self.start_camera_drag)
        self.accept("mouse1-up", self.stop_camera_drag)
        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)
        
        self.camera_dragging = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
        self.taskMgr.add(self.update_camera_task, "camera_update")
    
    def start_camera_drag(self):
        """Start camera drag operation."""
        self.camera_dragging = True
        if self.mouseWatcherNode.hasMouse():
            self.last_mouse_x = self.mouseWatcherNode.getMouseX()
            self.last_mouse_y = self.mouseWatcherNode.getMouseY()
    
    def stop_camera_drag(self):
        """Stop camera drag operation."""
        self.camera_dragging = False
    
    def zoom_in(self):
        """Zoom camera in."""
        self.camera_distance = max(2.0, self.camera_distance - 1.0)
    
    def zoom_out(self):
        """Zoom camera out."""
        self.camera_distance = min(50.0, self.camera_distance + 1.0)
    
    def update_camera_task(self, task: Task):
        """Update camera position based on controls."""
        if self.camera_dragging and self.mouseWatcherNode.hasMouse():
            mouse_x = self.mouseWatcherNode.getMouseX()
            mouse_y = self.mouseWatcherNode.getMouseY()
            
            dx = mouse_x - self.last_mouse_x
            dy = mouse_y - self.last_mouse_y
            
            self.camera_angle_h += dx * 100.0
            self.camera_angle_v = np.clip(self.camera_angle_v - dy * 100.0, -89.0, 89.0)
            
            self.last_mouse_x = mouse_x
            self.last_mouse_y = mouse_y
        
        # Calculate camera position
        h_rad = np.radians(self.camera_angle_h)
        v_rad = np.radians(self.camera_angle_v)
        
        x = self.camera_distance * np.cos(v_rad) * np.sin(h_rad)
        y = -self.camera_distance * np.cos(v_rad) * np.cos(h_rad)
        z = self.camera_distance * np.sin(v_rad)
        
        self.camera.setPos(
            self.camera_target.x + x,
            self.camera_target.y + y,
            self.camera_target.z + z
        )
        self.camera.lookAt(self.camera_target)
        
        return Task.cont
    
    def add_text_info(self, text: str, position: tuple = (0.05, 0.95)):
        """
        Add on-screen text information.
        
        Args:
            text: Text to display
            position: Screen position (x, y) in range [0, 1]
        """
        from direct.gui.OnscreenText import OnscreenText
        
        text_obj = OnscreenText(
            text=text,
            pos=(position[0] * 2 - 1, position[1] * 2 - 1),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=0,
            mayChange=True
        )
        return text_obj