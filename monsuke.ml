(*
** Download Fed Rates for analysis
*)

#load "unix.cma" ;;
open Unix ;;
let t = Unix.localtime (Unix.time ());;

let (day, month, year) = (t.tm_mday, t.tm_mon, t.tm_year) ;;
Printf.printf "The current date is %04d-%02d-%02d\n" (1900 + year) (month + 1) day ;;

let myURL = Printf.sprintf "http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=month(NEW_DATE)%%20eq%%2%02d%%20and%%20year(NEW_DATE)%%20eq%%20%02d" (month + 1) (1900 + year) in
    Unix.execvp "/usr/bin/wget" [|"wget"; myURL; "-O"; "/var/monsuke/rate.xml"|] ;;
