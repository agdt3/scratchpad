package;


class Hexes extends h2d.Graphics {

  public function drawHexes(
    width: Int,
    height: Int,
    rows: Int,
    columns: Int,
    ?spacing: Int = 0,
    ?color: Int = 0xFFFFFF
  ) {
    for (row in 0...rows) {
      for (col in 0...columns) {
        var hex = new Hex();
        hex.drawHex(width, height, color);

        var dy = row * (height + spacing) + Std.int(height / 2);
        var dx = col * (width + spacing - hex.xOffset);
        if (col % 2 == 0) {
          dy = row * (height + spacing);
        }

        /*
        var data = {
          "row": row,
          "col": col,
          "dx": dx,
          "dy": dy
        };
        trace(data);
        */

        hex.setPosition(dx, dy);
        addChild(hex);
      }
    }
  }

  public function findHex(point: h2d.col.Point): h2d.Object {
    var children = iterator();
    for (child in children) {
      //var bounds = h2d.col.Bounds(child.x, child.y, child.width, child.height);
      var bounds = child.getBounds();
      if (bounds.inside(point)) {
        return child;
      }
    }
  }
}


class Hex extends h2d.Graphics {
  public var xOffset: Int;
  public var bounds: h2d.col.Bounds;

  public function drawHex(
    width: Int,
    height: Int,
    ?color: Int = 0xFFFFFF,
    ?fixed: Bool = true
  ): Void {
    var halfHeight = height / 2;

    if (fixed) {
      var radians = 60 * Math.PI / 180;
      this.xOffset = Std.int(halfHeight / Math.tan(radians));
    } else {
      this.xOffset = Std.int(width / 4);
    }

    beginFill(color);
    lineTo(0, halfHeight);
    lineTo(xOffset, 0);
    lineTo(width - xOffset, 0);
    lineTo(width, halfHeight);
    lineTo(width - xOffset, height);
    lineTo(xOffset, height);
    lineTo(0, halfHeight);
    endFill();
  }
}
