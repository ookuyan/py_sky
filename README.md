# py_sky
Sky Brightness Model (Rayleigh and Mie Scattering)

# Examples

```python
from py_sky import set_scene, render, show


scene = set_scene(zenith=45, azimuth=180, width=32, height=32)

rgb = render(scene)

show(rgb)
```

![](https://raw.githubusercontent.com/ookuyan/py_sky/master/examples/sky_model.png?token=AAQLO5GNVY5BZ5KBBP5EWEK5BOQJS)
