@HIKE_DANGER_BIG_PR_LINES = 300

warn("Big PR! Pull Request size seems relatively large. If Pull Request contains multiple changes, split each into separate PR. This will help in faster and easier review.") if git.lines_of_code > @HIKE_DANGER_BIG_PR_LINES
warn('PR is classed as Work in Progress') if github.pr_title.include? '[WIP]'


if github.pr_body.length < 3 && git.lines_of_code > 10
  warn("Please provide a summary in the Pull Request description")
end


warn "#{github.html_link("build.gradle")} was edited." if git.modified_files.include? "build.gradle"
warn "#{github.html_link("AndroidManifest.xml")} was edited." if git.modified_files.include? "AndroidManifest.xml"
warn "#{github.html_link(".circleci/config.yml")} was edited." if git.modified_files.include? ".circleci/config.yml"

changed_file_count = github.pr_json["changed_files"]
changed_files_threshold = 15
warn "Number of changed files is #{changed_file_count}. Threshold is #{changed_files_threshold} files. Please break the PR into smaller chunks!" if changed_file_count > changed_files_threshold

findbugs_suppressed = false
findbugs_xml_modified = git.modified_files.include? "app/findbugs-filter.xml"

files_to_check = (git.modified_files + git.added_files - %w(Dangerfile))
git.added_files.each do |file|
    if File.exists?(file)
      file_size_in_kb = (File.size(file).to_f / 2**10).round(2)
      message "file size for #{file} : #{file_size_in_kb}KB"
      if File.size(file).to_f / 2**10 > 200
        failure "file size for #{file} : #{file_size_in_kb}KB is greater than 200KB"
      end
  end
end
files_to_check.each do |file|
  unless file.include? "Dangerfile"
    if git.diff_for_file(file).patch.include? "@SuppressFBWarnings"
      findbugs_suppressed = true
    end
  end
end

warn "Findbugs warning has been suppressed in this PR!" if findbugs_xml_modified || findbugs_suppressed
