{
  'variables': {
    'target_arch%': 'ia32',
    'library%': 'static_library',
    'msvs_mlti_core_compile': '0',
  },

  'target_defaults': {
    'default_configuration': 'Debug',
    'configurations': {
      'Debug': {
        'defines': [ 'DEBUG', '_DEBUG' ],
        'cflags': [ '-g', '-O0', '-fwrapv' ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'target_conditions': [
              ['library=="static_library"', {
                'RuntimeLibrary': 1, # static debug
              }, {
                'RuntimeLibrary': 3, # DLL debug
              }],
            ],
            'Optimization': 0, # /Od, no optimization
            'MinimalRebuild': 'false',
            'OmitFramePointers': 'false',
            'BasicRuntimeChecks': 3, # /RTC1
          },
          'VCLinkerTool': {
            'LinkIncremental': 2, # enable incremental linking
          },
        },
      },
      'Release': {
        'defines': [ 'NDEBUG' ],
        'cflags': [
          '-O3',
          '-fstrict-aliasing',
          '-fomit-frame-pointer',
          '-fdata-sections',
          '-ffunction-sections',
        ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'target_conditions': [
              ['library=="static_library"', {
                'RuntimeLibrary': 0, # static release
              }, {
                'RuntimeLibrary': 2, # debug eelease
              }],
            ],
            'Optimization': 3, # /Ox, full optimization
            'FavorSizeOrSpeed': 1, # /Ot, favor speed over size
            'InlineFunctionExpansion': 2, # /Ob2, inline anyting eligible
            'WholeProgramOptimization': 'true', # /GL, whole program optimization, needed for LTCG
            'OmitFramePointers': 'true',
            'EnableFunctionLevelLinking': 'true',
            'EnableIntrinsicFunctions': 'true',
          },
          'VCLibrarianTool': {
            'AdditionalOptions': [
              '/LTCG', # link time code generation
            ],
          },
          'VCLinkerTool': {
            'LinkTimeCodeGeneration': 1, # link-time code generation
            'OptimizeReferences': 2, # /OPT:REF
            'EnableCOMDATFolding': 2, # /OPT:ICF
            'LinkIncremental': 1, # disable incremental linking
          },
        },
      }
    },
    'msvs_settings': {
      'VCCLCompilerTool': {
        'StringPooling': 'true', # pool string literals
        'DebugInformationFormat': 3, # Generate a PDB
        'WarningLevel': 3,
        'BufferSecurityCheck': 'true',
        'ExceptionHandling': 1, # /EHsc
        'SuppressStartupBanner': 'true',
        'WarnAsError': 'false',
        'AdditionalOptions': [
          '/MP', # compile across multiple CPUs
        ],
      },
      'VCLibrarianTool': {
        'conditions': [
          ['target_arch=="x64"', {
            'TargetMachine': '17', # x64
          }, {
            'TargetMachine': '1',  # ia32
          }],
        ],
      },
      'VCLinkerTool': {
        'GenerateDebugInformation': 'true',
        'RandomizeBaseAddress': 2, # enable ASLR
        'DataExecutionPrevention': 2, # enable DEP
        'AllowIsolation': 'true',
        'SuppressStartupBanner': 'true',
        'target_conditions': [
          ['_type=="executable"', {
            'SubSystem': 1, # console executable
          }],
        ],
      },
    },
    'conditions': [
      ['OS == "win"', {
        'msvs_cygwin_shell': 0, # prevent actions from trying to use cygwin
        'defines': [
          'WIN32',
          # we don't really want VC++ warning us about
          # how dangerous C functions are...
          '_CRT_SECURE_NO_DEPRECATE',
          # ... or that C implementations shouldn't use
          # POSIX names
          '_CRT_NONSTDC_NO_DEPRECATE',
        ],
        'target_conditions': [
          ['target_arch=="x64"', {
            'msvs_configuration_platform': 'x64'
          }]
        ]
      }],
      ['OS in "freebsd linux"', {
        'cflags': [ '-Wall' ],
        'cflags_cc': [ '-fno-rtti', '-fno-exceptions' ],
        'target_conditions': [
          ['_type=="static_library"', {
            'standalone_static_library': 1, # disable thin archive which needs binutils >= 2.19
          }],
        ],
        'conditions': [
          [ 'target_arch=="x32"', {
            'cflags': [ '-mx32' ],
            'ldflags': [ '-mx32' ],
          }],
          [ 'OS=="linux"', {
            'cflags': [ '-ansi' ],
          }],
          [ 'OS not in "solaris android"', {
            'cflags': [ '-pthread' ],
            'ldflags': [ '-pthread' ],
          }],
          [ 'visibility=="hidden"', {
            'cflags': [ '-fvisibility==hidden' ],
          }],
        ],
      }],
    ],
  },
}
