AC_DICT_STRUCTURE = ["title", "title_ascii", "genre", "artist", "texture_title", "texture_artist", "texture_genre", "texture_load", "texture_list", "font_idx", "game_version", "other_folder", "bemani_folder", "splittable_diff", "SPB_diff", "SPN_diff", "SPH_diff", "SPA_diff", "SPL_diff", "DPB_diff", "DPN_diff", "DPH_diff", "DPA_diff", "DPL_diff", "unk_sect1", "unk_sect2", "unk_sect3", "song_id", "volume", "SPB_ident", "SPN_ident", "SPH_ident", "SPA_ident", "SPL_ident", "DPB_ident", "DPN_ident", "DPH_ident", "DPA_ident", "DPL_ident", "bga_delay", "bga_filename", "afp_flag", "afp_data0", "afp_data1", "afp_data2", "afp_data3", "afp_data4", "afp_data5", "afp_data6", "afp_data7", "afp_data8", "afp_data9", "unk_sect4"]

INF_DICT_STRUCTURE = ["title", "title_ascii", "genre", "artist", "texture_title", "texture_artist", "texture_genre", "texture_load", "texture_list", "font_idx", "game_version", "other_folder", "bemani_folder", "splittable_diff", "SPB_diff", "SPN_diff", "SPH_diff", "SPA_diff", "SPL_diff", "DPB_diff", "DPN_diff", "DPH_diff", "DPA_diff", "DPL_diff", "unk_sect1", "song_id", "volume", "SPB_ident", "SPN_ident", "SPH_ident", "SPA_ident", "SPL_ident", "DPB_ident", "DPN_ident", "DPH_ident", "DPA_ident", "DPL_ident", "bga_delay", "unk_sect2", "bga_filename", "unk_sect3", "afp_flag", "afp_data0", "afp_data1", "afp_data2", "afp_data3", "afp_data4", "afp_data5", "afp_data6", "afp_data7", "afp_data8", "afp_data9", "unk_sect4"]

AC_HEADER_FMTSTRING = "<4sIHH4x"
AC_CHART_FMTSTRING = "<64s64s64s64sIIIIIIHHHH10B6s480s160sII10cH32sI32s32s32s32s32s32s32s32s32s32s4s"
INF_HEADER_FMTSTRING = "<4sIII"
INF_CHART_FMTSTRING = "<64s64s64s64sIIIIIIHHHH10B326sII10cH2s32s2sI32s32s32s32s32s32s32s32s32s32s4s"

CONVERSION_DICT = {
	80001: 21265,
	80002: 28117,
	80003: 27203,
	80004: 28204,
	80005: 28205,
	80006: 28206,
	80007: 28207,
	80008: 28208,
	80009: 29096,
	80010: 28210,
	80011: 28211,
	80014: 29214,
	80015: 29215,
	80016: 29216,
	80017: 29217,
	80018: 29218,
	80019: 29219,
	80020: 29220,
	80021: 29221
}

SONG_POSSIBLE_DIFFS = ['SPB_diff', 'SPN_diff', 'SPH_diff', 'SPA_diff', 'SPL_diff',
'DPB_diff', 'DPN_diff',  'DPH_diff',  'DPA_diff', 'DPL_diff']