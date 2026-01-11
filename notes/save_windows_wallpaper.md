* Get lock screen background
  * Command Way
    * HotKey `Win + R` 
    * Input `%localappdata%\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets`
  * File Explorer Way
    * Open `File Explorer` 
    * Input `%localappdata%\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets`

* get desktop screen background
  * You can click `Start` button, input `Reg` keyword, you can find the `Registry` program, then click it
  * Ofcourse, if you only want to find registry, you can use hotkey `Win + R` to start `Run`, then input `Regedit`
  * Search the path `HKEY_CURRENT_USER\Control Panel\Desktop`, then input `Enter`
  * You can find the registry item `WallPaper`
  * Double click it, The value in the `Value data` field of the pop-up dialog box is the wallpaper path we are looking for