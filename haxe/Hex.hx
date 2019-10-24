package;

import h2d.col.Point;
import h2d.col.Polygon;
import h2d.col.Matrix;
import h2d.Object;
import h2d.Graphics;


class Hexes extends Graphics {

  public function drawHexes(
    width: Int,
    height: Int,
    rows: Int,
    columns: Int,
    ?spacing: Int = 0,
    ?baseColor: Int = 0xFFFFFF,
    ?selectedColor: Int = 0x808080,
    ?fixed: Bool = true
  ) {
    for (row in 0...rows) {
      for (col in 0...columns) {
        var hex = new Hex(width, height, baseColor, selectedColor, fixed);
        hex.drawHex();

        var dy = row * (height + spacing) + Std.int(height / 2);
        var dx = col * (width + spacing - hex.xOffset);
        if (col % 2 == 0) {
          dy = row * (height + spacing);
        }

        hex.updatePosition(dx, dy);
        addChild(hex);
      }
    }
  }

  public function findHexByPoint(point: Point): Null<Hex> {
    var children = iterator();
    var c: Null<Hex> = null;
    for (child in children) {
      if (!Std.is(child, Hex)) {
        continue;
      }

      var bounds = child.getBounds();
      if (bounds.contains(point)) {
        c = cast(child, Hex);
        if (c.collides(point)) {
          break;
        } else {
          c = null;
        }
      }
    }
    return c;
  }

  public function unselectAll() {
    var children = iterator();
    for (child in children) {
      if (!Std.is(child, Hex)) {
        continue;
      }

      var c = cast(child, Hex);
      if (c.selected) {
        c.unselect();
      }
    }
  }

  public function update() {
    var children = iterator();
    for (child in children) {
      if (!Std.is(child, Hex)) {
        continue;
      }

      var c = cast(child, Hex);
      if (c.dirty) {
        c.dirty = false;
        c.drawHex();
      }
    }
  }
}


class Hex extends Graphics {
  public var width: Int;
  public var height: Int;
  public var fixed: Bool;
  public var xOffset: Int;
  public var baseColor: Int;
  public var selectedColor: Int;
  public var currentColor: Int;
  public var dirty: Bool;
  public var selected: Bool;
  var collisionPolygon: Polygon;
  var points: Array<Point>;

  public function new(
    width: Int,
    height: Int,
    ?baseColor: Int = 0xFFFFFF,
    ?selectedColor: Int = 0x808080,
    ?fixed: Bool = true,
    ?parent: Object
  ) {
    super(parent);
    this.dirty = false;
    this.selected = false;
    this.width = width;
    this.height = height;

    this.currentColor = baseColor;
    this.baseColor = baseColor;
    this.selectedColor = selectedColor;

    this.fixed = fixed;
  }

  public function drawHex(): Void {
    var halfHeight = height / 2;

    if (fixed) {
      var radians = 60 * Math.PI / 180;
      this.xOffset = Std.int(halfHeight / Math.tan(radians));
    } else {
      this.xOffset = Std.int(width / 4);
    }

    points = new Array<Point>();
    points.push(new Point(0, halfHeight));
    points.push(new Point(xOffset, 0));
    points.push(new Point(width - xOffset, 0));
    points.push(new Point(width, halfHeight));
    points.push(new Point(width - xOffset, height));
    points.push(new Point(xOffset, height));
    points.push(new Point(0, halfHeight));

    if (collisionPolygon == null) {
      collisionPolygon = new Polygon(points);
    }

    beginFill(currentColor);
    for (point in points) {
      lineTo(point.x, point.y);
    }
    endFill();
  }

  public function select(): Void {
    if (!selected) {
      updateColor(selectedColor);
      selected = true;
    }
  }

  public function unselect(): Void {
    if (selected) {
      updateColor(baseColor);
      selected = false;
    }
  }

  public function collides(point: Point): Bool {
    return collisionPolygon.contains(point, true);
  }

  public function updateColor(color: Int): Void {
    this.currentColor = color;
    this.dirty = true;
  }

  public function updatePosition(x: Float, y: Float): Void {
    // from Object
    setPosition(x, y);

    var mat = new Matrix();
    mat.initTranslate(x, y);
    collisionPolygon.transform(mat);
  }

  override public function toString(): String {
    return 'Hex(w: $width h: $height color: $currentColor x: $x y: $y)';
  }
}
