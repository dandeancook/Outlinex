# Python
import re

# Modules
import sublime
from sublime        import Region
from sublime_plugin import WindowCommand, TextCommand, EventListener
from .show          import show, refresh_sym_view, get_sidebar_views_groups, get_sidebar_status, binary_search

def _____UTILS_____(): pass

# Index without exception
def idx(Value, Find):
    try:
        return Value.index(Find)
    except:
        return -1

def _____CLASSES_____(): pass
def _____COMMAND_____(): pass

#
class OutlineCommand(WindowCommand):

    #
    def run(self, immediate=False, single_pane=False, project=False, other_group=False, layout=0):
        show(self.window, single_pane=single_pane, other_group=other_group, layout=layout)

def _____SIDEBAR_____(): pass

#
class OutlineCloseSidebarCommand(WindowCommand):

    #
    def run(self):
        active_view = self.window.active_view()

        for v in self.window.views():
            if u'𝌆' in v.name():
                self.window.focus_view(v)
                self.window.run_command('close_file')

        self.window.set_layout({"cols": [0.0, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1]]})
        self.window.focus_view(active_view)

def _____REFRESH_____(): pass

#
class OutlineRefreshCommand(TextCommand):

    #
    def run(self, edit, symlist=None, symkeys=None, path=None, to_expand=None, toggle=None):
        self.view.erase(edit, Region(0, self.view.size()))

        if symlist and self.view.settings().get('outline_alphabetical'):
            symlist, symkeys = (list(t) for t in zip(*sorted(zip(symlist, symkeys))))

        # Dan D / Begin --------------------------------------------------------
        # Change region prefixes & item prefixes
        #
        Str         = "" # Debug value
        has_regions = False
        Is_Regions  = [False] * len(symlist)
        sublime.status_message("Outline shows "+str(len(symlist))+" symbols")

        # Find symbols to be indented, eg. variable functions
        Indented_Syms = []

        for i in range(len(symlist)):
            Name = symlist[i].strip()

            if idx(Name,"OX_INDENT_")==0: 
                Tokens = Name.replace("OX_INDENT_","").split("_")

                for j in range(len(Tokens)): 
                    if idx(Indented_Syms,Tokens[j].lower())==-1: 
                        Indented_Syms.append(Tokens[j].lower())
        # End for
        sublime.status_message("Indented symbols:\x20"+ ",\x20".join(Indented_Syms))

        # Mark symbols used for region names
        for i in range(len(symlist)):
            symlist[i] = symlist[i].strip()

            if idx(symlist[i],"#_____")==0 or idx(symlist[i],"$_____")==0 or \
                    idx(symlist[i],"_____")==0:
                has_regions   = True
                Is_Regions[i] = True

        # Render symbol list
        for i in range(len(symlist)):
            # Region item
            if idx(symlist[i],"#_____")==0 or idx(symlist[i],"$_____")==0 or \
                    idx(symlist[i],"_____")==0:
                # Change prefix to ⩥ & remove tail, change _ to -
                # True regex (with ^ for string start)
                symlist[i] = re.sub("#_____" , "⩥", symlist[i]);
                symlist[i] = re.sub("\$_____", "⩥", symlist[i]);
                symlist[i] = re.sub("^_____" , "⩥", symlist[i]);
                symlist[i] = re.sub("_+$"    , ""  , symlist[i]);

                # Blank line marker
                if idx(symlist[i].lower(), "⩥blank")==0:
                    symlist[i] = ""

                # Simple regex
                symlist[i] = symlist[i].replace(r"_", "-");

                # Add tail with corresponding length
                if len(symlist[i])>0:
                    while len(symlist[i])<20:
                        symlist[i] += "—" # Full-width dash, not minus sign

                # DEPRECATED: NO NEW LINE, SPOILS THE LINE VALUE TO GO TO SYMBOL
                #             WHEN CLICK.
                # No space before, if another region marker is right previous
                """
                if i>0 and Is_Regions[i-1]:
                    symlist[i] = symlist[i]
                else:                        
                    symlist[i] = "\n"+symlist[i]
                """

            # Regular item:    
            else:
                symlist[i] = re.sub("import\x20","#",symlist[i])

                # In a file with regions
                if has_regions: 
                    # Warn: Temp is not symlist[i]
                    Temp = symlist[i].strip().lower().replace("_","").replace("-","")

                    if idx(Temp,"oxindent")==0:
                        symlist[i] = "⩥Indented"
                    else:
                        Indent = ""

                        if idx(Indented_Syms,Temp)>=0 or idx(Temp.lower(),"case\x20")>=0: 
                            Indent="\u3000"
                        if idx(Temp.lower(),"case\x20")>=0:
                            symlist[i] = re.sub("case\x20", "$", symlist[i])
                            symlist[i] = re.sub('"',        "",  symlist[i])

                        # WARN: THIS IS NOT A REGULAR SPACE, A LARGE SPACE \u3000
                        # See:  https://en.wikipedia.org/wiki/Whitespace_character
                        symlist[i] = "\u3000"+Indent+symlist[i]

                # In a file without regions
                else: 
                    symlist[i] = "▸\x20"+symlist[i]
        # Dan D / End ----------------------------------------------------------

        # Show up
        Str = Str + ("\n".join(symlist))
        self.view.insert(edit, 0, Str)
        self.view.settings().set('symlist', symlist)
        self.view.settings().set('symkeys', symkeys)
        self.view.settings().set('current_file', path)
        self.view.sel().clear()

def _____TOGGLE_SORT_____(): pass

#
class OutlineToggleSortCommand(TextCommand):

    #
    def run(self, edit):
        sym_view = None

        for v in self.view.window().views():
            if u'𝌆' in v.name():
                v.settings().set('outline_alphabetical', not v.settings().get('outline_alphabetical'))
                sym_view = v

        symlist = self.view.get_symbols()
        refresh_sym_view(sym_view, symlist, self.view.file_name())

def _____EVENTS_____(): pass

#
class OutlineEventHandler(EventListener):

    #
    def on_selection_modified(self, view):
        if 'outline.hidden-tmLanguage' not in view.settings().get('syntax'):
            return

        sym_view, sym_group, fb_view, fb_group = get_sidebar_views_groups(view)
        sym_view     = view
        window       = view.window()
        sym_group, i = window.get_view_index(sym_view)
            
        if len(sym_view.sel()) == 0:
            return

        (row, col)  = sym_view.rowcol(sym_view.sel()[0].begin())
        active_view = None

        for group in range(window.num_groups()):
            if group != sym_group and group != fb_group:
                active_view = window.active_view_in_group(group)

        if active_view != None:
            symkeys = None
            # get the symbol list
            symlist = active_view.get_symbols()

            # depending on setting, set different regions
            if sym_view.settings().get('outline_main_view_highlight_mode') == 'cursor':
                symbol_line_ends = [active_view.line(range.a).end() for range, symbol in symlist]
                symkeys = list(zip(symbol_line_ends, symbol_line_ends))
            if sym_view.settings().get('outline_main_view_highlight_mode') == 'symbol':
                symkeys = sym_view.settings().get('symkeys')
            if sym_view.settings().get('outline_main_view_highlight_mode') == 'block':
                symbol_block_begins = [active_view.line(range.a).begin() for range, symbol in symlist]
                symbol_blocks_ends = [x - 1 for x in symbol_block_begins[1:len(symbol_block_begins)]] + [active_view.size()]
                symkeys = list(zip(symbol_block_begins, symbol_blocks_ends))
            if not symkeys:
                return

            region_position = symkeys[row]
            r = Region(region_position[0], region_position[1])
            active_view.show_at_center(r)
            active_view.sel().clear()
            active_view.sel().add(r)
            window.focus_view(active_view)

    #        
    def on_activated(self, view):
        if u'𝌆' in view.name():
            return
        # Avoid error message when console opens, as console is also a view, albeit with a group index of -1
        if view.window().get_view_index(view)[0] == -1:
            return
        if not get_sidebar_status(view):
            return

        sym_view, sym_group, fb_view, fb_group = get_sidebar_views_groups(view)

        if sym_view != None:
            if sym_view.settings().get('current_file') == view.file_name() and view.file_name() != None:
                return
            else:
                sym_view.settings().set('current_file', view.file_name())
            
        symlist = view.get_symbols()
        refresh_sym_view(sym_view, symlist, view.file_name())

    #    
    def on_pre_save(self, view):
        if u'𝌆' in view.name():
            return
        # this is not absolutely necessary, and prevents views that do not have a file reference from displaying 
        # the symbol list
        # but it solves a console error if the console is activiated, as console is also a view....
        if view.file_name() == None:
            return
        if not get_sidebar_status(view):
            return

        sym_view, sym_group, fb_view, fb_group = get_sidebar_views_groups(view)

        if sym_view != None:
            # Note here is the only place that differs from on_activate_view
            if sym_view.settings().get('current_file') != view.file_name():
                sym_view.settings().set('current_file', view.file_name())
            
        symlist = view.get_symbols()
        refresh_sym_view(sym_view, symlist, view.file_name())

        # sync the outline view with current file location
        if view.window() is None or not sym_view.settings().get('outline_sync'):
            return

        # get the current cursor location
        point = view.sel()[0].begin()
        # get the current symbol and its line in outline
        range_lows   = [view.line(range.a).begin() for range, symbol in symlist]
        range_sorted = [0] + range_lows[1:len(range_lows)] + [view.size()]
        sym_line     = binary_search(range_sorted, point) - 1

        if (sym_view is not None):
            sym_point_start = sym_view.text_point(sym_line, 0)
            # center symview at the point
            sym_view.show_at_center(sym_point_start)
            sym_view.sel().clear()
            sym_view.sel().add(sym_view.line(sym_point_start))
            view.window().focus_view(view)
    # End def
# End class
# EOF