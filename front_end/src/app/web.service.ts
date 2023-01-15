import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";

@Injectable()
export class WebService {
voter_list: any;
constructor(private http: HttpClient) {

  }
}
