require "tmpdir"

IGNORE_APIS = (ARGV.delete("--ignore-apis") != nil)
DETAILED    = (ARGV.delete("--detailed")    != nil)

# if ARGV.size == 2
FOLDER          = ARGV[0]
RULESET         = ARGV[1]
APIS            = ARGV[2]
GRAPHS_FOLDER   = ARGV[3]

FAST_SWITCH = true
# elsif ARGV.size > 2
#     puts "Unsupported"
#     exit
# else
#     raise "Too few arguments"
# end

THIS = File.dirname(__FILE__)

tmp = File.join Dir.tmpdir, "ruleset_" + rand(100000).to_s
while FileTest.exist? tmp
    tmp = File.join Dir.tmpdir, "ruleset_" + rand(100000).to_s
end

TMP = "."+tmp
raise "#{TMP}"
`mkdir -p #{TMP}`



