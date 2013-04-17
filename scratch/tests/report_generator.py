# -*- coding: utf-8 -*-
import re
from mechanize import Browser, ParseResponse, urlopen, urljoin
from traits.api import HasTraits, Property, cached_property, Event, \
    Array, Instance, Int, Directory, Range, on_trait_change, Bool, Trait, Constant, \
    Tuple, Interface, implements, Enum, Str, File, Button, on_trait_change
from traitsui.api import Item, View, HGroup, RangeEditor, Group, VGroup
from traitsui.menu import OKButton
from os.path import join, dirname
import os

API_KEY = 'AIzaSyCP-nYNoLGHaE7e9MuoupFQqTh2zDeGxQA'
UTRACK_API_KEY = 'ABQIAAAAWOh_axuONPjW1s6XecFT2RToNkpxhVZLfxutUbjc5IjsTEZ50RQTC0u2JCChM2JyX_kK0cxegop28g'

def test_dir(name):
    if os.access(name, os.F_OK)==False:
        os.mkdir(name)

class REPORT(HasTraits):
    ''' Generate report from GPX file using http://utrack.crempa.net/ and
        http://www.gpsvisualizer.com/
    '''
    title = Str()
    @on_trait_change( '+input_changed' )
    def _title_update(self):
        self.title = os.path.split(self.dirname)[-1]
        print self.title
    
    filename = File(input_changed = True, filter = ['*.gpx'])

    dirname = Property(Directory, depends_on = '+input_changed')
    def _get_dirname(self):
        return dirname(self.filename)

    convert = Bool(True, input_changet=True)

    conv_file_extension = Str('-converted')

    filename_converted = Property(File, depends_on = '+input_changed')
    def _get_filename_converted(self):
        if self.convert:
            return self.filename[:-4] + self.conv_file_extension + '.gpx'
        else:
            return self.filename
    
    gpx_convert = Button()
    def _gpx_convert_fired(self):
        ''' Convert gpx file to gpx to fix display problems in gps visualizer
        '''
        os.system('gpsbabel -t -i gpx -f "%s" -x nuketypes,waypoints,routes -o gpx,gpxver="1.0" -F "%s"' % (self.filename, self.filename_converted))
        print 'gpx converted'

    api_key = Str(API_KEY)
    
    download = Bool(True)
    
    utrack_gen = Button()
    def _utrack_gen_fired(self):
        test_dir(join(self.dirname,'img'))
        br = Browser()

        # Ignore robots.txt
        br.set_handle_robots( False )
        # Google demands a user-agent that isn't a robot
        br.addheaders = [('User-agent', 'Firefox')]
         
        # Retrieve the Google home page, saving the response
        resp1 = br.open( "http://utrack.crempa.net/index_cz.php" ) #http://utrack.crempa.net/index_en.php


        forms = ParseResponse(resp1, backwards_compat=False)
        form = forms[0]

        form.add_file(open(self.filename_converted), "text/plain", self.filename_converted)
        form.find_control(name='map_elevation').value = ['1']

        resp3=form.click()
        resp2 = urlopen(resp3).read()

        resp4 = br.open(resp3)

        if self.download:
            resp = None
            weblinks = list(br.links())
            imgi = 1
            for link in weblinks:
                siteMatch = re.compile( 'show_graph' ).search( link.url )
                if siteMatch:
                    imgfile = open(join(self.dirname,'img','%i.png') % imgi, 'wb')
                    resp = urlopen(link.absolute_url).read()
                    imgfile.write(resp)
                    imgfile.close()
                    imgi += 1
                    
            for link in weblinks:
                siteMatch = re.compile( 'report.php' ).search( link.url )
                if siteMatch:
                    pdffile = open(join(self.dirname,'img','report.pdf'), 'wb')
                    resp = urlopen(link.absolute_url).read()
                    pdffile.write(resp)
                    pdffile.close()

        # Print the site
        content = resp4.get_data()

        pattern = re.compile('src="show_graph.*?"')
        lst = pattern.findall(content)
        for ni, name in enumerate(lst):
            content = content.replace(name, 'src="img/%i.png"' % (ni+1))

        pattern = re.compile('href="show_graph.*?"')
        lst = pattern.findall(content)
        for ni, name in enumerate(lst):
            content = content.replace(name, 'href="img/%i.png"' % (ni+1))

        pattern = re.compile('Date of track: </td>\s+<td> (.*?) </td>')
        lst = pattern.findall(content)
        if len(lst) >= 2:
            if lst[0] != lst[-1]:
                track_date = lst[0] + '-' + lst[-1]
            else:
                track_date = lst[0]
        else:
            track_date = lst
        
        pattern = re.compile('href="report.php.*?"')
        lst = pattern.findall(content)
        content = content.replace(lst[0], 'href="img/report.pdf"')
        content = content.replace('<a href="#"', '<a href="#report_0"', 1)
        #content = content.replace('href="../style/style.css"', 'href="../style/style.css"')
        content = content.replace('src="../img/pdf.gif"', 'src="../style/pdf.gif"')
        content = content.replace('src="../img/logo.gif"', 'src="../style/logo.gif"')
        content = content.replace('src="../img/elegend.png"', 'src="../style/elegend.png"')
        #content = content.replace(r' >hide report</a>', r' >show report</a>')
        content = re.sub(r' >skr.*?t report</a>', r' >zobrazit report</a>', content)
        content = content.replace('if(divs[i].id==\'report_0\')', 'if(divs[i].id==\'report\')')
        content = content.replace(UTRACK_API_KEY, API_KEY)

        title = '<h1 style="margin-bottom:10px">%s <span style="font-size:small">%s</span></h1>\n' % (self.title,track_date)

        download_src = '''
        <a href="%s">Download source gpx file</a>
        ''' % os.path.basename(self.filename_converted)

        iframe_map_track = '''
        <iframe src="gps_vis/map_track.html" width="870" height="600" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" style="width: 870px; height: 600px; margin-top:10px; margin-left: 10px; margin-bottom: 10px; position: relative; overflow: hidden; font-family: arial,sans-serif; line-height: normal; padding: 0pt;">
          <a href="gps_vis/map_track.html">Click here for the map</a>
        </iframe>\n
        '''

        iframe_map_speed = '''
        <iframe src="gps_vis/map_speed.html" width="870" height="600" marginwidth="0" marginheight="0" scrolling="no" frameborder="0" style="width: 870px; height: 600px; margin-left: 10px; margin-bottom: 10px; position: relative; overflow: hidden; font-family: arial,sans-serif; line-height: normal; padding: 0pt;">
          <a href="gps_vis/map_speed.html">Click here for the map</a>
        </iframe>\n
        '''

        profile_img = '''
        <img src="gps_vis/profile.png" alt="profile" border="0" height="250" width="870" style="width: 870px; height: 250px; margin-left: 10px; margin-bottom: 10px; position: relative; overflow: hidden; font-family: arial,sans-serif; line-height: normal; padding: 0pt;">
        '''

        content = content.replace('<div id="page">', '<div id="page">\n' + title + iframe_map_track + profile_img)
        ofile = open(join(self.dirname,'track_report.html'),'w')
        ofile.write(content)
        ofile.close()
        br.close()

        print 'utrack generated'
    
    mapgen_track = Button()
    def _mapgen_track_fired(self):
        test_dir(join(self.dirname, 'gps_vis'))
        
        br = Browser()
        # Ignore robots.txt
        br.set_handle_robots( False )

        # Google demands a user-agent that isn't a robot
        br.addheaders = [('User-agent', 'Firefox')]
        
        resp1 = br.open( "http://www.gpsvisualizer.com/map_input" )
         
        # Select the search box and search for 'foo'
        br.select_form( name='main' )

        br.form['width'] = '870'
        br.form['height'] = '600'
        br.set_value(['google_openstreetmap'], name='bg_map')
        br.add_file(open(self.filename_converted), "text/plain", self.filename_converted, name='uploaded_file_1')
         
        # Get the search results
        resp2 = br.submit()
         
        resp = None
        for link in br.links():
            siteMatch = re.compile( 'download/' ).search( link.url )
            if siteMatch:
                resp = br.follow_link( link )
                break

        # Print the site
        content = resp.get_data()

        ofile = open(join(self.dirname, 'gps_vis', 'map_track.html'),'w')
        ofile.write(content)
        ofile.close()
        br.close()
        print 'map generated (track color)'
    
    mapgen_speed = Button()
    def _mapgen_speed_fired(self):
        test_dir(join(self.dirname, 'gps_vis'))
        br = Browser()
        # Ignore robots.txt
        br.set_handle_robots( False )

        # Google demands a user-agent that isn't a robot
        br.addheaders = [('User-agent', 'Firefox')]
            
        resp1 = br.open( "http://www.gpsvisualizer.com/map_input" )
         
        # Select the search box and search for 'foo'
        br.select_form( name='main' )

        br.form['width'] = '870'
        br.form['height'] = '600'
        br.set_value(['google_openstreetmap'], name='bg_map')
        br.set_value(['speed'], name='trk_colorize')
        br.form['legend_steps'] = '10'
        br.add_file(open(self.filename_converted), "text/plain", self.filename_converted, name='uploaded_file_1')
         
        # Get the search results
        resp2 = br.submit()
         
        resp = None
        for link in br.links():
            siteMatch = re.compile( 'download/' ).search( link.url )
            if siteMatch:
                resp = br.follow_link( link )
                break

        # Print the site
        content = resp.get_data()

        ofile = open(join(self.dirname, 'gps_vis', 'map_speed.html'),'w')
        ofile.write(content)
        ofile.close()
        br.close()

        print 'map generated (speed color)'
    
    profilegen = Button()
    def _profilegen_fired(self):
        test_dir(join(self.dirname, 'gps_vis'))
        br = Browser()
        # Ignore robots.txt
        br.set_handle_robots( False )

        # Google demands a user-agent that isn't a robot
        br.addheaders = [('User-agent', 'Firefox')]
            
        # Retrieve the Google home page, saving the response
        resp1 = br.open( "http://www.gpsvisualizer.com/profile_input" )
         
        # Select the search box and search for 'foo'
        br.select_form( name='main' )

        br.form['width'] = '870'
        br.form['height'] = '250'
        br.form['legend_steps'] = '10'
        br.add_file(open(self.filename_converted), "text/plain", self.filename_converted, name='uploaded_file_1')
         
        # Get the search results
        resp2 = br.submit()
         
        resp = None
        for link in br.links():
            siteMatch = re.compile( 'download/' ).search( link.url )
            if siteMatch:
                resp = br.follow_link( link )
                break

        # Print the site
        content = resp.get_data()

        ofile = open(join(self.dirname, 'gps_vis', 'profile.png'),'wb')
        ofile.write(content)
        ofile.close()
        br.close()

        print 'profile generated'

    traits_view = View( VGroup(
                        Group(
                            Item( 'title', springy = True ),
                            Item( 'filename', springy = True ),
                            Item( 'dirname', springy = True, style='readonly' ),
                            Item( 'conv_file_extension', springy = True, tooltip = 'If no extension specified, the original file will be overwrite.' ),
                            Item( 'filename_converted', springy = True, style='readonly' ),
                            Item( 'api_key', springy = True),
                            show_border = True,
                            label='settings',
                            ),
                        Group(
                            HGroup( Item( 'convert', label='convert gpx to gpx'),
                                    Item( 'gpx_convert',  label = 'gpx convert', show_label=False, springy = True, enabled_when='convert'),
                                    ),
                            HGroup( Item( 'download', label='download utrack report files' ),
                                    Item( 'utrack_gen',  label = 'generate utrack', show_label=False, springy = True, visible_when='download==False'),
                                    Item( 'utrack_gen',  label = 'generate utrack and download', show_label=False, springy = True, visible_when='download'),
                                    ),
                            Item( 'mapgen_track',  label = 'generate map (color track)', show_label=False),
                            Item( 'profilegen',  label = 'generate profile', show_label=False),
                            '_',
                            Item( 'mapgen_track',  label = 'generate map (speed color)', show_label=False),
                            show_border = True,
                            label='generate',
                            ),
                        ),
                        resizable = True,
                        width = .3,
                        height = .5,
                        buttons = [OKButton]
                        )

    
    



if __name__ == '__main__':
    report = REPORT()
    report.configure_traits()
    

