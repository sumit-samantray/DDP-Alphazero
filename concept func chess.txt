function end_game_evaluation(pos, nowinnable) {
  var v = 0;
  v += piece_value_eg(pos) - piece_value_eg(colorflip(pos));
  v += psqt_eg(pos) - psqt_eg(colorflip(pos));
  v += imbalance_total(pos);
  v += pawns_eg(pos) - pawns_eg(colorflip(pos));
  v += pieces_eg(pos) - pieces_eg(colorflip(pos));
  v += mobility_eg(pos) - mobility_eg(colorflip(pos));
  v += threats_eg(pos) - threats_eg(colorflip(pos));
  v += passed_eg(pos) - passed_eg(colorflip(pos));
  v += king_eg(pos) - king_eg(colorflip(pos));
  if (!nowinnable) v += winnable_total_eg(pos, v);
  return v;
}
function piece_value_eg(pos, square) {
  if (square == null) return sum(pos, piece_value_eg);
  return piece_value_bonus(pos, square, false);
}
function piece_value_bonus(pos, square, mg) {
  if (square == null) return sum(pos, piece_value_bonus);
  var a = mg ? [124, 781, 825, 1276, 2538]
             : [206, 854, 915, 1380, 2682];
  var i = "PNBRQ".indexOf(board(pos, square.x, square.y));
  if (i >= 0) return a[i];
  return 0;
}
function psqt_eg(pos, square) {
  if (square == null) return sum(pos, psqt_eg);
  return psqt_bonus(pos, square, false);
}
function psqt_bonus(pos, square, mg) {
  if (square == null) return sum(pos, psqt_bonus, mg);
  var bonus = mg ? [
    [[-175,-92,-74,-73],[-77,-41,-27,-15],[-61,-17,6,12],[-35,8,40,49],[-34,13,44,51],[-9,22,58,53],[-67,-27,4,37],[-201,-83,-56,-26]],
    [[-53,-5,-8,-23],[-15,8,19,4],[-7,21,-5,17],[-5,11,25,39],[-12,29,22,31],[-16,6,1,11],[-17,-14,5,0],[-48,1,-14,-23]],
    [[-31,-20,-14,-5],[-21,-13,-8,6],[-25,-11,-1,3],[-13,-5,-4,-6],[-27,-15,-4,3],[-22,-2,6,12],[-2,12,16,18],[-17,-19,-1,9]],
    [[3,-5,-5,4],[-3,5,8,12],[-3,6,13,7],[4,5,9,8],[0,14,12,5],[-4,10,6,8],[-5,6,10,8],[-2,-2,1,-2]],
    [[271,327,271,198],[278,303,234,179],[195,258,169,120],[164,190,138,98],[154,179,105,70],[123,145,81,31],[88,120,65,33],[59,89,45,-1]]
  ] : [
    [[-96,-65,-49,-21],[-67,-54,-18,8],[-40,-27,-8,29],[-35,-2,13,28],[-45,-16,9,39],[-51,-44,-16,17],[-69,-50,-51,12],[-100,-88,-56,-17]],
    [[-57,-30,-37,-12],[-37,-13,-17,1],[-16,-1,-2,10],[-20,-6,0,17],[-17,-1,-14,15],[-30,6,4,6],[-31,-20,-1,1],[-46,-42,-37,-24]],
    [[-9,-13,-10,-9],[-12,-9,-1,-2],[6,-8,-2,-6],[-6,1,-9,7],[-5,8,7,-6],[6,1,-7,10],[4,5,20,-5],[18,0,19,13]],
    [[-69,-57,-47,-26],[-55,-31,-22,-4],[-39,-18,-9,3],[-23,-3,13,24],[-29,-6,9,21],[-38,-18,-12,1],[-50,-27,-24,-8],[-75,-52,-43,-36]],
    [[1,45,85,76],[53,100,133,135],[88,130,169,175],[103,156,172,172],[96,166,199,199],[92,172,184,191],[47,121,116,131],[11,59,73,78]]
  ];
  var pbonus = mg ? 
    [[0,0,0,0,0,0,0,0],[3,3,10,19,16,19,7,-5],[-9,-15,11,15,32,22,5,-22],[-4,-23,6,20,40,17,4,-8],[13,0,-13,1,11,-2,-13,5],
     [5,-12,-7,22,-8,-5,-15,-8],[-7,7,-3,-13,5,-16,10,-8],[0,0,0,0,0,0,0,0]]:
    [[0,0,0,0,0,0,0,0],[-10,-6,10,0,14,7,-5,-19],[-10,-10,-10,4,4,3,-6,-4],[6,-2,-8,-4,-13,-12,-10,-9],[10,5,4,-5,-5,-5,14,9],
     [28,20,21,28,30,7,6,13],[0,-11,12,21,25,19,4,7],[0,0,0,0,0,0,0,0]];
  var i = "PNBRQK".indexOf(board(pos, square.x, square.y));
  if (i < 0) return 0;
  if (i == 0) return pbonus[7 - square.y][square.x];
  else return bonus[i-1][7 - square.y][Math.min(square.x, 7 - square.x)];
}
function imbalance_total(pos, square) {
  var v = 0;
  v += imbalance(pos) - imbalance(colorflip(pos));
  v += bishop_pair(pos) - bishop_pair(colorflip(pos));
  return (v / 16) << 0;
}
function imbalance(pos, square) {
  if (square == null) return sum(pos, imbalance);
  var qo = [[0],[40,38],[32,255,-62],[0,104,4,0],[-26,-2,47,105,-208],[-189,24,117,133,-134,-6]];
  var qt = [[0],[36,0],[9,63,0],[59,65,42,0],[46,39,24,-24,0],[97,100,-42,137,268,0]];
  var j = "XPNBRQxpnbrq".indexOf(board(pos, square.x, square.y));
  if (j < 0 || j > 5) return 0;
  var bishop = [0, 0], v = 0;
  for (var x = 0; x < 8; x++) {
    for (var y = 0; y < 8; y++) {
      var i = "XPNBRQxpnbrq".indexOf(board(pos, x, y));
      if (i < 0) continue;
      if (i == 9) bishop[0]++;
      if (i == 3) bishop[1]++;
      if (i % 6 > j) continue;
      if (i > 5) v += qt[j][i-6];
            else v += qo[j][i];
    }
  }
  if (bishop[0] > 1) v += qt[j][0];
  if (bishop[1] > 1) v += qo[j][0];
  return v;
}
function bishop_pair(pos, square) {
  if (bishop_count(pos) < 2) return 0;
  if (square == null) return 1438;
  return board(pos, square.x, square.y) == "B" ? 1 : 0;
}
function bishop_count(pos, square) {
  if (square == null) return sum(pos, bishop_count);
  if (board(pos, square.x, square.y) == "B") return 1;
  return 0;
}
function pawns_eg(pos, square) {
  if (square == null) return sum(pos, pawns_eg);
  var v = 0;
  if (doubled_isolated(pos, square)) v -= 56;
  else if (isolated(pos, square)) v -= 15;
  else if (backward(pos, square)) v -= 24;
  v -= doubled(pos, square) * 56;
  v += connected(pos, square) ?  connected_bonus(pos, square) * (rank(pos, square) - 3) / 4 << 0 : 0;
  v -= 27 * weak_unopposed_pawn(pos, square);
  v -= 56 * weak_lever(pos, square);
  v += [0,-4,4][blocked(pos, square)];
  return v;
}
function doubled_isolated(pos, square) {
  if (square == null) return sum(pos, doubled_isolated);
  if (board(pos, square.x, square.y) != "P") return 0;
  if (isolated(pos, square)) {
    var obe=0,eop=0,ene=0;
    for (var y = 0; y < 8; y++) {
      if (y > square.y && board(pos, square.x, y) == "P") obe++;
      if (y < square.y && board(pos, square.x, y) == "p") eop++;
      if (board(pos, square.x - 1, y) == "p"
       || board(pos, square.x + 1, y) == "p") ene++;
    }
    if (obe > 0 && ene == 0 && eop > 0) return 1;
  }
  return 0;

}
function isolated(pos, square) {
  if (square == null) return sum(pos, isolated);
  if (board(pos, square.x, square.y) != "P") return 0;
  for (var y = 0 ; y < 8; y++) {
    if (board(pos, square.x - 1, y) == "P") return 0;
    if (board(pos, square.x + 1, y) == "P") return 0;
  }
  return 1;
}
function isolated(pos, square) {
  if (square == null) return sum(pos, isolated);
  if (board(pos, square.x, square.y) != "P") return 0;
  for (var y = 0 ; y < 8; y++) {
    if (board(pos, square.x - 1, y) == "P") return 0;
    if (board(pos, square.x + 1, y) == "P") return 0;
  }
  return 1;
}
function backward(pos, square) {
  if (square == null) return sum(pos, backward);
  if (board(pos, square.x, square.y) != "P") return 0;
  for (var y = square.y; y < 8; y++) {
    if (board(pos, square.x - 1, y) == "P"
     || board(pos, square.x + 1, y) == "P") return 0;
  }
  if (board(pos, square.x - 1, square.y - 2) == "p"
   || board(pos, square.x + 1, square.y - 2) == "p"
   || board(pos, square.x    , square.y - 1) == "p") return 1;
  return 0;
}
function doubled(pos, square) {
  if (square == null) return sum(pos, doubled);
  if (board(pos, square.x, square.y) != "P") return 0;
  if (board(pos, square.x, square.y + 1) != "P") return 0;
  if (board(pos, square.x - 1, square.y + 1) == "P") return 0;
  if (board(pos, square.x + 1, square.y + 1) == "P") return 0;
  return 1;
}
function connected(pos, square) {
  if (square == null) return sum(pos, connected);
  if (supported(pos, square) || phalanx(pos, square)) return 1;
  return 0;
}
function supported(pos, square) {
  if (square == null) return sum(pos, supported);
  if (board(pos, square.x, square.y) != "P") return 0;
  return (board(pos, square.x - 1, square.y + 1) == "P" ? 1 : 0)
       + (board(pos, square.x + 1, square.y + 1) == "P" ? 1 : 0);
}
function phalanx(pos, square) {
  if (square == null) return sum(pos, phalanx);
  if (board(pos, square.x, square.y) != "P") return 0;
  if (board(pos, square.x - 1, square.y) == "P") return 1;
  if (board(pos, square.x + 1, square.y) == "P") return 1;
  return 0;
}
function connected_bonus(pos, square) {
  if (square == null) return sum(pos, connected_bonus);
  if (!connected(pos, square)) return 0;
  var seed = [0, 7, 8, 12, 29, 48, 86];
  var op = opposed(pos, square);
  var ph = phalanx(pos, square);
  var su = supported(pos, square);
  var bl = board(pos, square.x, square.y - 1) == "p" ? 1 : 0;
  var r = rank(pos, square);
  if (r < 2 || r > 7) return 0;
  return seed[r - 1] * (2 + ph - op) + 21 * su;
}
function opposed(pos, square) {
  if (square == null) return sum(pos, opposed);
  if (board(pos, square.x, square.y) != "P") return 0;
  for (var y = 0; y < square.y; y++) {
    if (board(pos, square.x, y) == "p") return 1;
  }
  return 0;
}
function rank(pos, square) {
  if (square == null) return sum(pos, rank);
  return 8 - square.y;
}
function weak_unopposed_pawn(pos, square) {
  if (square == null) return sum(pos, weak_unopposed_pawn);
  if (opposed(pos, square)) return 0;
  var v = 0;
  if (isolated(pos, square)) v++;
  else if (backward(pos, square)) v++;
  return v;
}
function weak_lever(pos, square) {
  if (square == null) return sum(pos, weak_lever);
  if (board(pos, square.x, square.y) != "P") return 0;
  if (board(pos, square.x - 1, square.y - 1) != "p") return 0;
  if (board(pos, square.x + 1, square.y - 1) != "p") return 0;
  if (board(pos, square.x - 1, square.y + 1) == "P") return 0;
  if (board(pos, square.x + 1, square.y + 1) == "P") return 0;
  return 1;
}
function blocked(pos, square) {
  if (square == null) return sum(pos, blocked);
  if (board(pos, square.x, square.y) != "P") return 0;
  if (square.y != 2 && square.y != 3) return 0;
  if (board(pos, square.x, square.y - 1) != "p") return 0;
  return 4 - square.y;
}
function passed_eg(pos, square) {
  if (square == null) return sum(pos, passed_eg);
  if (!passed_leverable(pos, square)) return 0;
  var v = 0;
  v += king_proximity(pos, square);
  v += [0,28,33,41,72,177,260][passed_rank(pos, square)];
  v += passed_block(pos, square);
  v -= 8 * passed_file(pos, square);
  return v;
}
function passed_leverable(pos, square) {
  if (square == null) return sum(pos, passed_leverable);
  if (!candidate_passed(pos, square)) return 0;
  if (board(pos, square.x, square.y - 1) != "p") return 1;
  var pos2 = colorflip(pos);
  for (var i = -1; i <=1; i+=2) {
    var s1 = {x:square.x + i, y:square.y};
    var s2 = {x:square.x + i, y:7-square.y};
    if (board(pos, square.x + i, square.y + 1) == "P"
     && "pnbrqk".indexOf(board(pos, square.x + i, square.y)) < 0
     && (attack(pos, s1) > 0 || attack(pos2, s2) <= 1)
    ) return 1;
  }
  return 0;
}
function candidate_passed(pos, square) {
  if (square == null) return sum(pos, candidate_passed);
  if (board(pos, square.x, square.y) != "P") return 0;
  var ty1 = 8, ty2 = 8, oy = 8;
  for (var y = square.y - 1; y >= 0; y--) {
    if (board(pos, square.x    , y) == "P") return 0;
    if (board(pos, square.x    , y) == "p") ty1 = y;
    if (board(pos, square.x - 1, y) == "p"
     || board(pos, square.x + 1, y) == "p") ty2 = y;
  }
  if (ty1 == 8 && ty2 >= square.y - 1) return 1;
  if (ty2 < square.y - 2 || ty1 < square.y - 1) return 0;
  if (ty2 >= square.y && ty1 == square.y - 1 && square.y < 4) {
    if (board(pos, square.x - 1, square.y + 1) == "P"
     && board(pos, square.x - 1, square.y    ) != "p"
     && board(pos, square.x - 2, square.y - 1) != "p") return 1;
    if (board(pos, square.x + 1, square.y + 1) == "P"
     && board(pos, square.x + 1, square.y    ) != "p"
     && board(pos, square.x + 2, square.y - 1) != "p") return 1;
  }
  if (board(pos, square.x, square.y - 1) == "p") return 0;
  var lever = (board(pos, square.x - 1, square.y - 1) == "p" ? 1 : 0)
             + (board(pos, square.x + 1, square.y - 1) == "p" ? 1 : 0);
  var leverpush = (board(pos, square.x - 1, square.y - 2) == "p" ? 1 : 0)
                + (board(pos, square.x + 1, square.y - 2) == "p" ? 1 : 0);
  var phalanx = (board(pos, square.x - 1, square.y) == "P" ? 1 : 0)
              + (board(pos, square.x + 1, square.y) == "P" ? 1 : 0);
  if (lever - supported(pos, square) > 1) return 0;
  if (leverpush - phalanx  > 0) return 0;
  if (lever > 0 && leverpush > 0) return 0;
  return 1;
}
function king_proximity(pos, square) {
  if (square == null) return sum(pos, king_proximity);
  if (!passed_leverable(pos, square)) return 0;
  var r = rank(pos, square)-1;
  var w = r > 2 ? 5 * r - 13 : 0;
  var v = 0;
  if (w <= 0) return 0;
  for (var x = 0; x < 8; x++) {
    for (var y = 0; y < 8; y++) {
      if (board(pos, x, y) == "k") {
        v += ((Math.min(Math.max(Math.abs(y - square.y + 1),
                        Math.abs(x - square.x)),5) * 19 / 4) << 0) * w;
      }
      if (board(pos, x, y) == "K") {
        v -= Math.min(Math.max(Math.abs(y - square.y + 1),
                      Math.abs(x - square.x)),5) * 2 * w;
        if (square.y > 1) {
          v -= Math.min(Math.max(Math.abs(y - square.y + 2),
                      Math.abs(x - square.x)),5) * w;
        }
      }
    }
  }
  return v;
}
function passed_rank(pos, square) {
  if (square == null) return sum(pos, passed_rank);
  if (!passed_leverable(pos, square)) return 0;
  return rank(pos, square) - 1;
}
function attack(pos, square) {
  if (square == null) return sum(pos, attack);
  var v = 0;
  v += pawn_attack(pos, square);
  v += king_attack(pos, square);
  return v;
}
function pawn_attack(pos, square) {
  if (square == null) return sum(pos, pawn_attack);
  var v = 0;
  if (board(pos, square.x - 1, square.y + 1) == "P") v++;
  if (board(pos, square.x + 1, square.y + 1) == "P") v++;
  return v;
}
function king_attack(pos, square) {
  if (square == null) return sum(pos, king_attack);
  for (var i = 0; i < 8; i++) {
    var ix = (i + (i > 3)) % 3 - 1;
    var iy = (((i + (i > 3)) / 3) << 0) - 1;
    if (board(pos, square.x + ix, square.y + iy) == "K") return 1;
  }
  
 
  return 0;
}
function passed_block(pos, square) {
  if (square == null) return sum(pos, passed_block);
  if (!passed_leverable(pos, square)) return 0;
  if (rank(pos, square) < 4) return 0;
  if (board(pos, square.x, square.y - 1) != "-") return 0;
  var r = rank(pos, square) - 1;
  var w = r > 2 ? 5 * r - 13 : 0;
  var pos2 = colorflip(pos);
  var defended = 0, unsafe = 0, wunsafe = 0, defended1 = 0, unsafe1 = 0;
  for (var y = square.y - 1; y >= 0; y--) {
    if (attack(pos, {x:square.x,y:y})) defended++;
    if (attack(pos2, {x:square.x,y:7-y})) unsafe++;
    if (attack(pos2, {x:square.x-1,y:7-y})) wunsafe++;
    if (attack(pos2, {x:square.x+1,y:7-y})) wunsafe++;
    if (y == square.y - 1) {
      defended1 = defended;
      unsafe1 = unsafe;
    }
  }
  for (var y = square.y + 1; y < 8; y++) {
    if (board(pos, square.x, y) == "R"
     || board(pos, square.x, y) == "Q") defended1 = defended = square.y;
    if (board(pos, square.x, y) == "r"
     || board(pos, square.x, y) == "q") unsafe1 = unsafe = square.y;
  }
  var k = (unsafe == 0 && wunsafe == 0 ? 35 : unsafe == 0 ? 20 : unsafe1 == 0 ? 9 : 0)
        + (defended1 != 0 ? 5 : 0);
  return k * w;
}
function passed_file(pos, square) {
  if (square == null) return sum(pos, passed_file);
  if (!passed_leverable(pos, square)) return 0;
  var file = file(pos, square);
  return Math.min(file - 1, 8 - file);
}
function file(pos, square) {
  if (square == null) return sum(pos, file);
  return 1 + square.x;
}
function king_eg(pos) {
  var v = 0;
  v -= 16 * king_pawn_distance(pos);
  v += endgame_shelter(pos);
  v += 95 * pawnless_flank(pos);
  return v;
}
function king_pawn_distance(pos, square) {
  var v = 6, kx = 0, ky = 0, px = 0, py = 0;
  for (var x = 0; x < 8; x++) {
    for (var y = 0; y < 8; y++) {
      if (board(pos, x, y) == "K") {
        kx = x;
        ky = y;
      }
    }
  }
  for (var x = 0; x < 8; x++) {
    for (var y = 0; y < 8; y++) {
      var dist = Math.max(Math.abs(x-kx),Math.abs(y-ky));
      if (board(pos, x, y) == "P" && dist < v) { px = x; py = y; v = dist; }
    }
  }
  if (square == null || square.x == px && square.y == py) return v;
  return 0;
}
function endgame_shelter(pos, square) {
  var w = 0, s = 1024, tx = null;
  for (var x = 0; x < 8; x++) {
    for (var y = 0; y < 8; y++) {
      if (board(pos, x, y) == "k"
       || pos.c[2] && x == 6 && y == 0
       || pos.c[3] && x == 2 && y == 0) {
        var w1 = strength_square(pos, {x:x,y:y});
        var s1 = storm_square(pos, {x:x,y:y});
        var e1 = storm_square(pos, {x:x,y:y}, true);
        if (s1 - w1 < s - w) { w = w1; s = s1; e = e1; }
      }
    }
  }
  if (square == null) return e;
  return 0;
}
function strength_square(pos, square) {
  if (square == null) return sum(pos, strength_square);
  var v = 5;
  var kx = Math.min(6, Math.max(1, square.x));
  var weakness =
      [[-6,81,93,58,39,18,25],
      [-43,61,35,-49,-29,-11,-63],
      [-10,75,23,-2,32,3,-45],
      [-39,-13,-29,-52,-48,-67,-166]];
  for (var x = kx - 1; x <= kx +1; x++) {
    var us = 0;
    for (var y = 7; y >= square.y; y--) {
      if (board(pos, x, y) == "p"


       && board(pos, x-1, y+1) != "P"
       && board(pos, x+1, y+1) != "P") us = y;
    }
    var f = Math.min(x, 7 - x);
    v += weakness[f][us] || 0;
  }
  return v;
}
function storm_square(pos, square, eg) {
  if (square == null) return sum(pos, storm_square);
  var v = 0, ev = 5;
  var kx = Math.min(6, Math.max(1, square.x));
  var unblockedstorm = [
    [85,-289,-166,97,50,45,50],
    [46,-25,122,45,37,-10,20],
    [-6,51,168,34,-2,-22,-14],
    [-15,-11,101,4,11,-15,-29]];
  var blockedstorm = [
    [0,0,76,-10,-7,-4,-1],
    [0,0,78,15,10,6,2]];
  for (var x = kx - 1; x <= kx +1; x++) {
    var us = 0, them = 0;
    for (var y = 7; y >= square.y; y--) {
      if (board(pos, x, y) == "p"
       && board(pos, x-1, y+1) != "P"
       && board(pos, x+1, y+1) != "P") us = y;
      if (board(pos, x, y) == "P") them = y;
    }
    var f = Math.min(x, 7 - x);
    if (us > 0 && them == us + 1) {
      v += blockedstorm[0][them];
      ev += blockedstorm[1][them];
    }
    else v += unblockedstorm[f][them];
  }
  return eg ? ev : v;
}
function pawnless_flank(pos) {
  var pawns=[0,0,0,0,0,0,0,0], kx = 0;
  for (var x = 0; x < 8; x++) {
    for (var y = 0; y < 8; y++) {
      if (board(pos, x, y).toUpperCase() == "P") pawns[x]++;
      if (board(pos, x, y) == "k") kx = x;
    }
  }
  var sum;
  if (kx == 0) sum = pawns[0] + pawns[1] + pawns[2];
  else if (kx < 3) sum = pawns[0] + pawns[1] + pawns[2] + pawns[3];
  else if (kx < 5) sum = pawns[2] + pawns[3] + pawns[4] + pawns[5];
  else if (kx < 7) sum = pawns[4] + pawns[5] + pawns[6] + pawns[7];
  else  sum = pawns[5] + pawns[6] + pawns[7];
  return sum == 0 ? 1 : 0;
}
