import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VoteService {

  constructor(private http: HttpClient) { }

  voteForCandidate(voter_id: number, candidate_id: number) {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
    });
    const data = {
      voter_id: voter_id,
      candidate_id: candidate_id
  };
    console.log('Sending request with data:', data);
    return this.http.post('http://localhost:5000/api/v1.0/votes', JSON.stringify(data), { headers: headers });
  }
}
