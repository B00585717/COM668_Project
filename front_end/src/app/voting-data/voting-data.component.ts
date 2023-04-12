import {Component, OnInit} from '@angular/core';
import {WebService} from '../services/web.service';
import Chart from 'chart.js/auto';

@Component({
  selector: 'voting-data',
  templateUrl: './voting-data.component.html',
  styleUrls: ['./voting-data.component.css']
})
export class VotingDataComponent implements OnInit {
  votingData: any[] = [];
  public votingPieChart: any;
  public votingBarChart: any;
  public partyVotingPieChart: any;
  public partyVotingBarChart: any;
  groupedData: any;

  constructor(private webService: WebService) { }

  ngOnInit(): void {
    this.webService.getVotingData().subscribe((data: any) => {
      this.votingData = data;
      this.createPieChart()
      this.createBarChart()

      this.groupedData = this.votingData.reduce((accumulator, current) => {
      const existingParty = accumulator.find((party: { party_name: any; }) => party.party_name === current.party_name);

      if (existingParty) {
        existingParty.vote_count += current.vote_count;
        existingParty.vote_percentage += current.vote_percentage;
      } else {
        accumulator.push(current);
      }

      return accumulator;
    }, []);

      this.createPartyBarChart()
      this.createPartyPieChart()
    });
  }

  calculateVotePercentage(vote_count: number): number {
  const totalVotes = this.votingData.reduce((total, candidate) => total + candidate.vote_count, 0);
  return (vote_count / totalVotes) * 100;
}
  sortByVotePercentage(): void {
    this.votingData.sort((a, b) => b.vote_percentage - a.vote_percentage);
  }

  createPieChart(){
    const candidateNames = this.votingData.map(candidate => candidate.candidate_name);
    const colors = this.getColours(candidateNames.length);
      this.votingPieChart = new Chart("votingPieChart", {
        type: 'doughnut',

        data: {
          labels: candidateNames,
           datasets: [
            {
              label: "Vote Percentage",
              data: this.votingData.map(candidate => candidate.vote_percentage),
              backgroundColor: colors
            },
          ]
        },
        options: {
          aspectRatio:1
        }
      });
  }

  createBarChart(){
    const candidateNames = this.votingData.map(candidate => candidate.candidate_name);
    const colors = this.getColours(candidateNames.length);
      this.votingBarChart = new Chart("votingBarChart", {
        type: 'bar',

        data: {
          labels: candidateNames,
           datasets: [
            {
              label: "Vote Percentage",
              data: this.votingData.map(candidate => candidate.vote_percentage),
              backgroundColor: colors
            },
          ]
        },
        options: {
          aspectRatio:1
        }
      });
  }

  createPartyPieChart() {
  const partyNames = this.groupedData.map((party: { party_name: any; }) => party.party_name);
  const colors = this.getColours(partyNames.length);
  this.partyVotingPieChart = new Chart("partyVotingPieChart", {
    type: 'doughnut',

    data: {
      labels: partyNames,
      datasets: [
        {
          label: "Vote Percentage",
          data: this.groupedData.map((party: { vote_percentage: any; }) => party.vote_percentage),
          backgroundColor: colors
        },
      ]
    },
    options: {
      aspectRatio: 1
    }
  });
  }

  createPartyBarChart() {
    const partyNames = this.groupedData.map((party: { party_name: any; }) => party.party_name);
    const colors = this.getColours(partyNames.length);
    this.partyVotingBarChart = new Chart("partyVotingBarChart", {
      type: 'bar',

      data: {
        labels: partyNames,
        datasets: [
          {
            label: "Vote Percentage",
            data: this.groupedData.map((party: { vote_percentage: any; }) => party.vote_percentage),
            backgroundColor: colors
          },
        ]
      },
      options: {
        aspectRatio: 1
      }
    });
  }
  getColours(count: number) {
    return ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'black', 'lilac', 'gold'];
}

}
