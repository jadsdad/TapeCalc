#!/usr/bin/python3

import sys
from logtools_common import logtools_common as common
from tapecalcui import Ui_Dialog
from PyQt5 import QtWidgets

class TapeCalcForm(Ui_Dialog):
    def __init__(self, ui, conn):
        Ui_Dialog.__init__(self)
        self.setupUi(ui)

        self.conn = conn
        self.populateArtCombo()
        self.populateAlbCombo()
        self.populateLengths()
        self.populateExtra()

        self.cmbArtist.currentIndexChanged.connect(self.populateAlbCombo)
        self.cmbAlbum.currentIndexChanged.connect(self.do_calculation)
        self.cmbExtra.currentIndexChanged.connect(self.do_calculation)
        self.cmbLength.currentIndexChanged.connect(self.do_calculation)
        self.evenSides.stateChanged.connect(self.do_calculation)
        self.chkAllowBonus.stateChanged.connect(self.do_calculation)
        self.cmdComplete.clicked.connect(self.markAsRecorded)


    def markAsRecorded(self):
        alb_id = int(self.cmbAlbum.itemData(self.cmbAlbum.currentIndex()))
        c = self.conn.cursor()
        c.execute("UPDATE album SET RecordedToCassette='Y' "
                                       "WHERE albumid={};".format(alb_id))
        self.conn.commit()

        self.populateAlbCombo()

    def populateArtCombo(self):
        c = self.conn.cursor()
        c.execute("SELECT DISTINCT artist.artistid, artistname "
                  "FROM artist "
                  "INNER JOIN albumartist on artist.artistid = albumartist.artistid "
                  "INNER JOIN album on album.albumid = albumartist.albumid "
                  "WHERE album.sourceid in (4) AND album.AlbumTypeID <> 8 "
                  "AND album.albumid not in (select albumid from albums_missing_tracks) "
                  "AND album.recordedtocassette is null "
                  "ORDER BY artistname;")
        artlist = c.fetchall()
        self.cmbArtist.clear()
        for a in artlist:
            self.cmbArtist.addItem(a[1], a[0])

    def populateAlbCombo(self):
        art_id = self.getSelectedArtist()
        c = self.conn.cursor()
        c.execute("SELECT album.albumid, album from album "
                  "inner join albumartist on album.albumid = albumartist.albumid "
                  "WHERE artistid={} and SourceID in (4) AND recordedtocassette is null and "
                  "album.albumid not in (select albumid from albums_missing_tracks)"
                  "order by album;".format(art_id))
        alblist = c.fetchall()
        self.cmbAlbum.clear()
        for a in alblist:
            self.cmbAlbum.addItem(a[1], a[0])

    def populateLengths(self):
        lengths=[15, 23, 30, 37, 45, 50, 60]
        for l in lengths:
            self.cmbLength.addItem("{}min (C{})".format(l, l*2), str(l))

    def populateExtra(self):
        self.cmbExtra.addItem("None","0")
        self.cmbExtra.addItem("1 min", "60")
        self.cmbExtra.addItem("1.5 min", "90")
        self.cmbExtra.addItem("2 min", "120")
        self.cmbExtra.addItem("2.5 min", "150")

    def getSelectedArtist(self):
        if self.cmbArtist.count() > 0:
            art_id = int(self.cmbArtist.itemData(self.cmbArtist.currentIndex()))
            return art_id
        else:
            return 0

    def getSelectedAlbum(self):
        if self.cmbAlbum.count() > 0:
            alb_id = int(self.cmbAlbum.itemData(self.cmbAlbum.currentIndex()))
            return alb_id
        else:
            return 0

    def getSideLength(self):
        side_length = int(self.cmbLength.itemData(self.cmbLength.currentIndex()))
        return int(side_length) * 60

    def allowExtra(self):
        return int(self.cmbExtra.itemData(self.cmbExtra.currentIndex()))

    def attemptEven(self):
        return self.evenSides.isChecked()

    def allowBonus(self):
        return self.chkAllowBonus.isChecked()

    def do_calculation(self):
        if self.cmbAlbum.count() > 0:
            c = Calculator()
            output = c.do_calculation(self.getSelectedAlbum(), self.getSideLength() + self.allowExtra(),
                                      self.attemptEven(), self.allowBonus())
            self.txtOutput.setText(output)

class Track:
    def __init__(self):
        self.track_no = 0
        self.track_title = ""
        self.track_time = 0

class Side:
    def __init__(self):
        self.side_no = 0
        self.tracks = []
        self.totaltime = 0
        self.trackcount = 0

    def add_track(self, t):
        self.tracks.append(t)
        self.totaltime += t.track_time
        self.trackcount = len(self.tracks)

class Calculator:

    def get_rows_from_sql(self, sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def convert_to_ms(self, time_seconds):
        minutes = time_seconds // 60
        seconds = time_seconds % 60
        return "{:02d}:{:02d}".format(minutes, seconds)

    def get_track_list(self, album_id, allowbonus):
        sql = "SELECT disc, track, tracktitle, tracklength " \
              "FROM tracklengths " \
              "WHERE AlbumID={} ".format(album_id)

        if not allowbonus:
            sql += "AND bonustrack = 0 "

        sql += "ORDER BY disc, track;"
        tracklist = self.get_rows_from_sql(sql)
        return tracklist

    def get_album_length(self, tracklist):
        subtotal = 0
        for t in tracklist:
            subtotal += t[3]
        return subtotal

    def add_track_to_side(self, trk, s, trackindex):
        s.add_track(trk)
        return trackindex + 1

    def start_new_side(self, sides, s, sideindex):
        sides.append(s)
        sideindex += 1
        s = Side()
        s.side_no = sideindex
        return s, sideindex

    def do_calculation(self, album_id, side_length, aimforeven, allowbonus):

        # Make a note of the original tape length selected and the total
        # album length if we're aiming for even sides.
        orig_side_length = side_length
        tracklist = self.get_track_list(album_id, allowbonus)
        albumlength = self.get_album_length(tracklist)

        output = ""

        # if we're aiming for even sides, and it won't all fit on one side,
        # work out the target side length by dividing the total album time
        # by the actual side length to get how many sides are needed, then divide
        # the total length by the number of sides. Add 5% to be on the
        # safe side. If this takes the side length over what was originally
        # selected, go with the maximum side length.

        if aimforeven and (albumlength > side_length):
            sides_needed = albumlength // side_length + 1
            side_length = int(albumlength // sides_needed)
            evenmin = side_length - (side_length // 20)
            eventarget = side_length + (side_length // 20)
            evenmax = side_length + (side_length // 10)
            evenmax = orig_side_length if evenmax > orig_side_length else evenmax

            print("Aiming for {} sides of approx {}".format(sides_needed, self.convert_to_ms(eventarget)))

        trackindex = 1
        sideindex = 1
        sides = []
        s = Side()
        s.side_no = 1

        for t in tracklist:
            trk = Track()
            trk.track_no = trackindex
            trk.track_title = t[2]
            trk.track_time = t[3]

            if trk.track_time > orig_side_length:
                return "One track is longer than the tape length will allow.\n" \
                       "Please select a different tape length."

            startnewside = False
            if aimforeven and albumlength > orig_side_length:
                if (trk.track_no > 1) and (s.totaltime + trk.track_time in range(evenmin, eventarget)):
                    trackindex = self.add_track_to_side(trk, s, trackindex)
                    s, sideindex = self.start_new_side(sides, s, sideindex)

                elif (trk.track_no > 1) and (s.totaltime + trk.track_time in range(eventarget, evenmax)):
                    trackindex = self.add_track_to_side(trk, s, trackindex)
                    s, sideindex = self.start_new_side(sides, s, sideindex)

                elif (trk.track_no > 1) and (s.totaltime + trk.track_time > evenmax)\
                        or (s.totaltime + trk.track_time > orig_side_length):
                    s, sideindex = self.start_new_side(sides, s, sideindex)
                    trackindex = self.add_track_to_side(trk, s, trackindex)

                else:
                    trackindex = self.add_track_to_side(trk, s, trackindex)
            else:
                if (trk.track_no > 1) and (s.totaltime + trk.track_time > side_length):
                    s, sideindex = self.start_new_side(sides, s, sideindex)
                    trackindex = self.add_track_to_side(trk, s, trackindex)
                else:
                    trackindex = self.add_track_to_side(trk, s, trackindex)

        sides.append(s)

        lastside = sides[-1]

        if len(lastside.tracks) == 0:
            sides.remove(lastside)
            lastside = sides[-1]

        if len(sides) > 1:
            if lastside.totaltime < (orig_side_length - sides[-2].totaltime):
                for t in lastside.tracks:
                    sides[-2].add_track(t)

                sides.remove(lastside)
                lastside = sides[-1]

        for s in sides:
            output += "SIDE {}: {}\n\n".format(s.side_no, self.convert_to_ms(s.totaltime))
            for t in s.tracks:
                output += "{}. {} ({})\n".format(t.track_no, t.track_title, self.convert_to_ms(t.track_time))
            output += "\n"

        if not aimforeven:
            timeleft = (orig_side_length) - lastside.totaltime
            timeleftstr = self.convert_to_ms(timeleft)

            output += "Time remaining at end of Side {}: {}".format(lastside.side_no, timeleftstr)

        return output


if __name__ == "__main__":
    conn = common.conn
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = TapeCalcForm(dialog, conn)
    dialog.show()
    sys.exit(app.exec())
