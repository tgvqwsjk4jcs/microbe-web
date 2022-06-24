#!/usr/bin/haserl --upload-limit=5120 --upload-dir=/tmp
<%in p/common.cgi %>
<%
sysupgrade_date=$(ls -lc --full-time /usr/sbin/sysupgrade | xargs | cut -d' ' -f6)
sysupgrade_date=$(date +"%s" --date="$sysupgrade_date")

file="$POST_parts_file"
file_name="$POST_parts_file_name"
error=""

case "$POST_parts_type" in
kernel)
  maxsize=2097152
  magicnum="27051956"
  new_sysupgrade_date=$(date +"%s" --date="2021-12-07")
  cmd="sysupgrade --kernel=/tmp/${file_name} --force_ver"
  ;;
rootfs)
  maxsize=5242880
  magicnum="68737173"
  new_sysupgrade_date=$(date +"%s" --date="2022-02-22")
  cmd="sysupgrade --rootfs=/tmp/${file_name} --force_ver --force_all"
  ;;
*)
  error="Please select type of file and upload it again!"
  ;;
esac

[ -z "$file_name"  ] && error="$t_form_error_1"
[ ! -r "$file" ] && error="$t_form_error_2"
[ "$(wc -c $file | awk '{print $1}')" -gt "$maxsize" ] && error="$t_form_error_3 $(wc -c $file | awk '{print $1}') > ${maxsize}."
[ "$magicnum" -ne "$(xxd -p -l 4 $file)" ] && error="$t_form_error_4 $(xxd -p -l 4 $file) != $magicnum"
[ "$sysupgrade_date" -lt "$new_sysupgrade_date" ] && error="$t_form_error_5"

if [ -n "$error" ]; then
  redirect_back "danger" "$error"
else %>
<%in p/header.cgi %>
<%
  pre_ "bg-light p-4 log-scroll"
    xl "mv $file /tmp/${file_name}"
    $cmd
  _pre
  button_home
fi
%>
<%in p/footer.cgi %>
