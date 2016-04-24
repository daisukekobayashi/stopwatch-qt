{ 'includes': [
    'common.gypi',
  ],
  'variables': {
    'qt_sdk%': 'C:/Qt/4.8.7',
    'conditions': [
      ['OS == "linux"', {
      }],
      ['OS == "win"', {
        'qt_moc': '<(qt_sdk)/bin/moc.exe',
        'qt_uic': '<(qt_sdk)/bin/uic.exe',
        'qt_includes': [
          '<(qt_sdk)/include',
          '<(qt_sdk)/include/QtGui',
          '<(qt_sdk)/include/QtCore',
        ],
        'qt_lib_dirs': [
          '<(qt_sdk)/lib',
        ],
        'qt_libs': [
          '-lQtCore4',
          '-lQtGui4',
        ],
      }],
    ],
    'moc_src_dir': './src',
    'moc_gen_dir': './moc',
  },
  'targets': [
    {
      'target_name': 'stopwatch',
      'type': 'executable',
      'dependencies': [
        #'uic',
        'mocs',
      ],
      'include_dirs': [
        'include',
        'src/',
        '<@(qt_includes)',
      ],
      'conditions': [
        ['OS != "win"', {
          'defines': [
            '_LARGEFILE_SOURCE',
            '_FILE_OFFSET_BITS=64',
          ],
        }],
        ['OS in "mac ios"', {
          'defines': [ '_DARWIN_USE_64_BIT_INODE=1' ],
        }],
        ['OS == "linux"', {
          'defines': [ '_POSIX_C_SOURCE=200112' ],
        }],
      ],
      'sources': [
        'src/main.cc',
        'src/stopwatch.h',
        'src/stopwatch.cc',
        'src/main-window.h',
        'src/main-window.cc',
        '<(moc_gen_dir)/moc-stopwatch.cc',
        '<(moc_gen_dir)/moc-main-window.cc'
      ],
      'conditions': [
        ['OS =="win"', {
          'defines': [
            '_WIN32_WINNT=0x0600',
            '_GNU_SOURCE',
          ],
          'sources': [
          ],
          'conditions': [
            ['MSVS_VERSION < "2015"', {
              'sources': [
              ]
            }]
          ],
          'link_settings': {
            'libraries': [
              '-ladvapi32',
              '-liphlpapi',
              '-lpsapi',
              '-lshell32',
              '-luserenv',
              '-lws2_32',
              '<@(qt_libs)',
            ],
            'library_dirs': [
              '<@(qt_lib_dirs)',
            ],
          },
        }, { # Not Windows i.e. POSIX
          'cflags': [
            '-g',
            '-std=c++11',
            '-pedantic',
            '-Wall',
            '-Wextra',
            '-Wno-unused-parameter',
          ],
          'sources': [
          ],
          'link_settings': {
            'libraries': [ '-lm' ],
            'conditions': [
              ['OS != "solaris" and OS != "android"', {
                'ldflags': [ '-pthread' ],
              }],
            ],
          },
        }],
        ['OS in "linux mac ios android"', {
          'sources': [
          ],
        }],
        ['OS == "linux"', {
          'defines': [ '_GNU_SOURCE' ],
          'sources': [
          ],
          'link_settings': {
            'libraries': [ '-ldl', '-lrt' ],
          },
        }],
      ]
    },
    {
      'target_name': 'mocs',
      'type': 'none',
      'sources': [
        '<(moc_src_dir)/main-window.h',
        '<(moc_src_dir)/stopwatch.h',
      ],
      'rules': [
        {
          'rule_name': 'generate_moc',
          'extension': 'h',
          'outputs': [ '<(moc_gen_dir)/moc-<(RULE_INPUT_ROOT).cc' ],
          'action': [ '<(qt_moc)', '<(RULE_INPUT_PATH)', '-o',
                      '<(moc_gen_dir)/moc-<(RULE_INPUT_ROOT).cc' ],
          'message': 'Generating moc-<(RULE_INPUT_ROOT).cc from <(RULE_INPUT_PATH).',
        },
      ],
    },
  ],
}
