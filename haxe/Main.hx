import Hex.Hexes;
import Hex.Hex;


class Main extends hxd.App {
  var hexes: Hexes;

  override function init() {
    trace(s2d.width);
    trace(s2d.height);
    hexes = new Hexes(s2d);
    hexes.drawHexes(100, 100, 4, 10, 2, 0xEA8220, 0xEBAE75);
    var bounds = hexes.getBounds();
    var interaction = new h2d.Interactive(bounds.width, bounds.height, hexes);
    /*
    interaction.onMove = function(event: hxd.Event) {
      var selectedHex = hexes.findHexByPoint(new h2d.col.Point(event.relX, event.relY));
      if (selectedHex != null) {
        hexes.unselectAll();
        selectedHex.select();
      }
    }
    */
    interaction.onClick = function(event: hxd.Event) {
      var selectedHex = hexes.findHexByPoint(new h2d.col.Point(event.relX, event.relY));
      if (selectedHex != null) {
        hexes.unselectAll();
        selectedHex.select();
      }
    }
  }
  // on each frame
  override function update(dt:Float) {
    hexes.update();
  }

  static function main() {
    new Main();
  }
}
