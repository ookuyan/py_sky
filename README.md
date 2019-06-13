# py_sky
Sky Brightness Model (Rayleigh and Mie Scattering)

# Examples

```python
from py_sky import set_scene, render, show


scene = set_scene(zenith=45, azimuth=180, width=32, height=32)

rgb = render(scene)

show(rgb)
```

![alt ](https://drive.google.com/open?id=1o9H9RFzTfLzr7dQOdMNBtYuD7lQpw4kO)
