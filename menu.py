def _hex_to_nuke_color(hex_color):
    hex_color = hex_color.lstrip("#")
    return int(hex_color + "00", 16)  # Nuke format: 0xRRGGBB00


def _normalize_label(text):
    if not text:
        return ""
    return " ".join(str(text).strip().lower().split())


def _set_pref_color_by_label(prefs, target_labels, color_value):
    target_labels = {_normalize_label(x) for x in target_labels}

    for knob in prefs.knobs().values():
        try:
            label = _normalize_label(knob.label())
            name = _normalize_label(knob.name())

            if label in target_labels or name in target_labels:
                knob.setValue(color_value)
        except Exception:
            pass


def _apply_nuke_dark_palette():
    try:
        import nuke

        if nuke.NUKE_VERSION_MAJOR >= 16:
            from PySide6.QtWidgets import QApplication
            from PySide6.QtGui import QPalette, QColor
        else:
            from PySide2.QtWidgets import QApplication
            from PySide2.QtGui import QPalette, QColor

        app = QApplication.instance()
        if not app:
            return

        palette = app.palette()

        # Core backgrounds
        palette.setColor(QPalette.Window, QColor("#121212"))
        palette.setColor(QPalette.Base, QColor("#0e0e0e"))
        palette.setColor(QPalette.AlternateBase, QColor("#151515"))
        palette.setColor(QPalette.Button, QColor("#181818"))

        # Depth / bevel tones
        palette.setColor(QPalette.Light, QColor("#222222"))
        palette.setColor(QPalette.Midlight, QColor("#1c1c1c"))
        palette.setColor(QPalette.Dark, QColor("#0a0a0a"))
        palette.setColor(QPalette.Mid, QColor("#262626"))
        palette.setColor(QPalette.Shadow, QColor("#050505"))

        # Text
        palette.setColor(QPalette.WindowText, QColor("#cfcfcf"))
        palette.setColor(QPalette.Text, QColor("#d8d8d8"))
        palette.setColor(QPalette.ButtonText, QColor("#d2d2d2"))
        palette.setColor(QPalette.BrightText, QColor("#ffffff"))

        # Selection / focus
        palette.setColor(QPalette.Highlight, QColor("#2a2a2a"))
        palette.setColor(QPalette.HighlightedText, QColor("#f3f3f3"))

        try:
            palette.setColor(QPalette.PlaceholderText, QColor("#7e7e7e"))
        except Exception:
            pass

        app.setPalette(palette)

        prefs = nuke.toNode("preferences")
        if not prefs:
            return

        # Keep your DAG background only
        if "DAGBackColor" in prefs.knobs():
            prefs["DAGBackColor"].setValue(_hex_to_nuke_color("#0d0d0d"))

        # Only line/arrow visibility colors
        arrow_line = _hex_to_nuke_color("#7a7a7a")
        elbow_line = _hex_to_nuke_color("#969696e")

        # DO NOT touch "Node Graph" or "Overlay"
        _set_pref_color_by_label(prefs, ["Elbow"], elbow_line)

        # Main arrow colors
        _set_pref_color_by_label(prefs, ["←", "→", "↑", "↓"], arrow_line)

        # Extra arrow-related colors
        _set_pref_color_by_label(prefs, ["deep arrows"], arrow_line)
        _set_pref_color_by_label(prefs, ["expression arrows"], arrow_line)
        _set_pref_color_by_label(prefs, ["link knob arrows"], arrow_line)
        _set_pref_color_by_label(prefs, ["link node arrows"], arrow_line)
        _set_pref_color_by_label(prefs, ["clone arrows"], arrow_line)

    except Exception:
        import traceback
        traceback.print_exc()


_apply_nuke_dark_palette()