import Hex.Hexes;

class Main extends hxd.App {
  override function init() {
    var hexes = new Hexes(s2d);
    hexes.drawHexes(100, 100, 4, 10, 2, 0xEA8220);
    var bounds = hexes.getBounds();
    var interaction = new h2d.Interactive(bounds.width, bounds.height, hexes);
    interaction.onOver = function(event: hxd.Event) {
      trace(event);
    }
  }
  // on each frame
  override function update(dt:Float) {

  }

  static function main() {
    new Main();
  }
}
