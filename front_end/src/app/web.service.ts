import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";

@Injectable()
export class WebService {
voter_list: any;
constructor(private http: HttpClient) {
  }

  getCandidates() {
    return this.http.get('http://localhost:5000/api/v1.0/candidates').subscribe((response: any) => {
 this.voter_list = response;
 console.log(response)
 });
  }
}
