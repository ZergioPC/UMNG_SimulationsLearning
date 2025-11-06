import numpy as np
from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, AmbientLight, DirectionalLight, Vec3, Vec4
from direct.task import Task


class PandaRender(ShowBase):
    """
    A Panda3D renderer that displays objects with xyz attributes.
    Objects can be updated dynamically and the renderer will reflect changes.
    """
    
    def __init__(self):
        super().__init__()
        
        # Dictionary to store object references and their visual representations
        self.tracked_objects = {}
        
        # Set up camera
        self.camera.setPos(0, -20, 10)
        self.camera.lookAt(0, 0, 0)
        
        # Set up lighting
        self.setup_camera()
        self._setup_lighting()
        
        # Add update task
        self.taskMgr.add(self.update_objects, "UpdateObjectsTask")
             
    def _setup_lighting(self):
        """Configure scene lighting"""
        # Ambient light
        ambient = AmbientLight("ambient")
        ambient.setColor(Vec4(0.3, 0.3, 0.3, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)
        
        # Directional light
        directional = DirectionalLight("directional")
        directional.setColor(Vec4(0.8, 0.8, 0.8, 1))
        directional_np = self.render.attachNewNode(directional)
        directional_np.setHpr(45, -45, 0)
        self.render.setLight(directional_np)
    
    def add_object(self, obj, model_path="models/box", scale=1.0, color=None):
        """
        Add an object to be rendered.
        
        Args:
            obj: Object with x, y, z attributes
            model_path: Path to the 3D model (default: "models/box")
            scale: Scale of the model
            color: Optional color tuple (r, g, b, a) with values 0-1
        """
        if obj in self.tracked_objects:
            return  # Object already tracked
        
        # Load the model
        model = self.loader.loadModel(model_path)
        model.reparentTo(self.render)
        model.setScale(scale)
        
        # Set color if provided
        if color:
            model.setColor(*color)
        
        # Set initial position
        model.setPos(obj.x[0], obj.x[1], obj.x[2])
        
        # Store reference
        self.tracked_objects[obj] = model
    
    def remove_object(self, obj):
        """Remove an object from the renderer"""
        if obj in self.tracked_objects:
            self.tracked_objects[obj].removeNode()
            del self.tracked_objects[obj]
    
    def update_objects(self, task):
        """Update all tracked objects' positions (called every frame)"""
        for obj, model in self.tracked_objects.items():
            # Update position based on object's current xyz attributes
            model.setPos(obj.x[0], obj.x[1], obj.x[2])
        
        return Task.cont
    
    def setup_camera(self):
        """Configure camera position and orientation."""
        self.disableMouse()
        self.camera.setPos(0, -15, 5)
        self.camera.lookAt(0, 0, 0)

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