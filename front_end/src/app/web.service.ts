import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";

@Injectable()
export class WebService {
constructor(private http: HttpClient) {}

  addVoter(voter: any) {
    let formData = this.formData(voter);
    return this.http.post('http://localhost:5000/api/v1.0/register', formData);
  }

  private formData(voter: any) {

    let formData = new FormData();
    formData.append("first_name", voter.first_name);
    formData.append("last_name", voter.last_name);
    formData.append("email", voter.email);
    formData.append("password", voter.password);

    return formData;
  }
}
