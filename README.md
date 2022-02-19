picom.conf #Fix screan tearing on Asus

```
backend = "glx";
glx-no-stencil = true;
glx-no-rebind-pixmap = true;
vsync = true;
xrender-sync-fence = "true";
glx-swap-method = -1;
```
